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
    def __init__(self, state, wrapped=False):
        self.state = state
        self.wrapped = wrapped

    def execute(self, query, params):
        self.last = (query, params)

    def fetchall(self):
        self.state['fetch_calls'] += 1
        if self.state['fetch_calls'] == 1:
            if self.wrapped:
                raise RuntimeError("'utf-8' codec can't decode byte 0xf3 in position 85: invalid continuation byte")
            raise UnicodeDecodeError('utf-8', b'\xf3', 0, 1, 'invalid start byte')
        return [{'id_cliente': 1, 'activo': True}]

    def close(self):
        pass


class FakeDB:
    def __init__(self, wrapped=False):
        self.rollback_calls = 0
        self.encoding_calls = []
        self.state = {'fetch_calls': 0}
        self.current_encoding = 'UTF8'
        self.wrapped = wrapped

    def get_cursor(self):
        return FakeCursor(self.state, wrapped=self.wrapped)

    def rollback(self):
        self.rollback_calls += 1

    def set_client_encoding(self, encoding):
        self.current_encoding = encoding
        self.encoding_calls.append(encoding)

    def get_client_encoding(self):
        return self.current_encoding

    def reconnect(self, preferred_encoding=None):
        if preferred_encoding:
            self.set_client_encoding(preferred_encoding)

    def obtener_encodings_preferidos(self):
        return ['UTF8', 'LATIN1']


def _assert_retry_behaviour(fake_db):
    dao = FakeDAO()
    rows = dao.listar_todos()

    assert rows == [{'id_cliente': 1, 'activo': True}]
    assert fake_db.rollback_calls == 1
    assert 'LATIN1' in fake_db.encoding_calls
    assert fake_db.get_client_encoding() == 'UTF8'



def test_fetch_retry_on_unicode_error(monkeypatch):
    fake_db = FakeDB(wrapped=False)
    monkeypatch.setattr('app.dao.base_dao.db', fake_db)
    _assert_retry_behaviour(fake_db)


def test_fetch_retry_on_wrapped_unicode_message(monkeypatch):
    fake_db = FakeDB(wrapped=True)
    monkeypatch.setattr('app.dao.base_dao.db', fake_db)
    _assert_retry_behaviour(fake_db)
