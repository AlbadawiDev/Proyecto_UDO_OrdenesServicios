"""Offline regressions for one bounded read retry; no database credentials."""
import psycopg2
import pytest

from app.config import Config
from app.dao.base_dao import BaseDAO


class DAO(BaseDAO):
    tabla = 'synthetic_catalog'
    primary_key = 'id'

    def mapear_a_objeto(self, row):
        return row


class Cursor:
    def __init__(self, db, error):
        self.db, self.error, self.closed = db, error, False

    def execute(self, query, params):
        self.db.queries.append((query, params))

    def fetchall(self):
        if self.error:
            raise self.error
        return [{'id': 1, 'description': 'synthetic'}]

    def fetchone(self):
        return self.fetchall()[0]

    def close(self):
        self.closed = True


class DB:
    def __init__(self, errors):
        self.errors = list(errors)
        self.encoding = 'UTF8'
        self.encoding_calls, self.cursors, self.queries = [], [], []
        self.rollback_calls = 0
        self.closed = False
        self.fail_restore = False

    def get_cursor(self):
        cursor = Cursor(self, self.errors.pop(0) if self.errors else None)
        self.cursors.append(cursor)
        return cursor

    def get_client_encoding(self):
        return self.encoding

    def set_client_encoding(self, value):
        self.encoding_calls.append(value)
        if self.fail_restore and value == 'UTF8':
            raise RuntimeError('synthetic encoding restore failure')
        self.encoding = value

    def rollback(self):
        self.rollback_calls += 1

    def cerrar(self):
        self.closed = True


def unicode_error():
    return UnicodeDecodeError('utf-8', b'\xf3', 0, 1, 'invalid continuation byte')


def wrapped(kind):
    outer = RuntimeError('synthetic adapter wrapper')
    if kind == 'cause':
        outer.__cause__ = unicode_error()
    elif kind == 'context':
        outer.__context__ = unicode_error()
    else:
        outer = RuntimeError("'utf-8' codec can't decode byte 0xf3 in position 1: invalid continuation byte")
    return outer


@pytest.mark.parametrize('kind', ['cause', 'context', 'message'])
def test_wrapped_read_recovers_and_restores(monkeypatch, kind):
    db = DB([wrapped(kind), None])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    assert DAO().listar_todos() == [{'id': 1, 'description': 'synthetic'}]
    assert db.encoding_calls == ['LATIN1', 'UTF8']
    assert db.rollback_calls == 1
    assert len(db.queries) == 2
    assert all(c.closed for c in db.cursors)


def test_fetch_one_recovers_wrapped_error(monkeypatch):
    db = DB([wrapped('cause'), None])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    assert DAO().buscar_por_id(1)['id'] == 1
    assert db.encoding == 'UTF8'
    assert db.queries[0][1] == (1,)


@pytest.mark.parametrize('error', [psycopg2.ProgrammingError('synthetic SQL syntax failure'),
    psycopg2.ProgrammingError("'utf-8' codec can't decode byte 0xf3: invalid continuation byte"),
    RuntimeError('synthetic invalid continuation byte in non-decoding task')])
def test_unrelated_failures_do_not_retry(monkeypatch, error):
    db = DB([error])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    with pytest.raises(type(error)) as caught:
        DAO().listar_todos()
    assert caught.value is error
    assert len(db.queries) == 1
    assert not db.encoding_calls
    assert db.rollback_calls == 0
    assert db.cursors[0].closed


def test_cyclic_cause_terminates_without_retry(monkeypatch):
    error = RuntimeError('synthetic cyclic wrapper')
    error.__cause__ = error
    db = DB([error])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    with pytest.raises(RuntimeError):
        DAO().listar_todos()
    assert len(db.queries) == 1
    assert db.cursors[0].closed


@pytest.mark.parametrize('link', ['__cause__', '__context__'])
def test_sql_wrapper_with_decoding_text_does_not_retry(monkeypatch, link):
    error = wrapped('message')
    setattr(error, link, psycopg2.ProgrammingError('synthetic underlying SQL failure'))
    db = DB([error])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    with pytest.raises(RuntimeError) as caught:
        DAO().listar_todos()
    assert caught.value is error
    assert len(db.queries) == 1
    assert not db.encoding_calls
    assert db.rollback_calls == 0
    assert db.cursors[0].closed


def test_retry_failure_rolls_back_and_restores(monkeypatch):
    db = DB([wrapped('cause'), psycopg2.ProgrammingError('synthetic retry failure')])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    with pytest.raises(psycopg2.ProgrammingError):
        DAO().listar_todos()
    assert db.encoding_calls == ['LATIN1', 'UTF8']
    assert db.rollback_calls == 2
    assert all(c.closed for c in db.cursors)


def test_same_fallback_does_not_repeat_identical_read(monkeypatch):
    db = DB([unicode_error()])
    monkeypatch.setattr(Config, 'DB_FALLBACK_ENCODING', 'UTF8')
    monkeypatch.setattr('app.dao.base_dao.db', db)
    with pytest.raises(UnicodeDecodeError):
        DAO().listar_todos()
    assert len(db.queries) == 1
    assert not db.encoding_calls


def test_failed_restore_discards_connection(monkeypatch):
    db = DB([wrapped('cause'), None])
    db.fail_restore = True
    monkeypatch.setattr('app.dao.base_dao.db', db)
    with pytest.raises(RuntimeError, match='synthetic encoding restore failure'):
        DAO().listar_todos()
    assert db.closed
    assert all(c.closed for c in db.cursors)


def test_normal_read_does_not_change_encoding(monkeypatch):
    db = DB([None])
    monkeypatch.setattr('app.dao.base_dao.db', db)
    assert DAO().listar_todos()[0]['id'] == 1
    assert not db.encoding_calls
    assert db.rollback_calls == 0
    assert db.cursors[0].closed
