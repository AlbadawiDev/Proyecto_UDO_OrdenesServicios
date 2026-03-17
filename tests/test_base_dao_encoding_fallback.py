from app.dao.base_dao import BaseDAO


class FakeDAO(BaseDAO):
    @property
    def tabla(self):
        return 'cliente'

    @property
    def primary_key(self):
        return 'id_cliente'

    def mapear_a_objeto(self, fila):
        return fila


class FakeCursor:
    def __init__(self, state):
        self.state = state

    def execute(self, query, params):
        self.last = (query, params)

    def fetchall(self):
        self.state['fetch_calls'] += 1
        if self.state['fetch_calls'] == 1:
            raise UnicodeDecodeError('utf-8', b'\xf3', 0, 1, 'invalid start byte')
        return [{'id_cliente': 1, 'activo': True}]

    def close(self):
        pass


class FakeDB:
    def __init__(self):
        self.rollback_calls = 0
        self.encoding_calls = []
        self.state = {'fetch_calls': 0}

    def get_cursor(self):
        return FakeCursor(self.state)

    def rollback(self):
        self.rollback_calls += 1

    def set_client_encoding(self, encoding):
        self.encoding_calls.append(encoding)


def test_fetch_retry_on_unicode_error(monkeypatch):
    fake_db = FakeDB()
    monkeypatch.setattr('app.dao.base_dao.db', fake_db)

    dao = FakeDAO()
    rows = dao.listar_todos()

    assert rows == [{'id_cliente': 1, 'activo': True}]
    assert fake_db.rollback_calls == 1
    assert fake_db.encoding_calls[-1] == 'LATIN1'
