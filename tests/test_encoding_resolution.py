from app.dao.conexion import ConexionDB


class _Cursor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query):
        self.query = query

    def fetchone(self):
        return ['UTF8']


class _Conn:
    closed = False

    def cursor(self):
        return _Cursor()


def test_obtener_encodings_preferidos_incluye_fallbacks(monkeypatch):
    monkeypatch.setattr('app.dao.conexion.Config.DB_CLIENT_ENCODING', 'utf8')
    monkeypatch.setattr('app.dao.conexion.Config.DB_FALLBACK_ENCODING', 'latin1')
    monkeypatch.setattr('app.dao.conexion.Config.DB_EXTRA_FALLBACK_ENCODINGS', 'win1252,latin1')

    db = ConexionDB()
    encodings = db.obtener_encodings_preferidos()

    assert encodings == ['UTF8', 'LATIN1', 'WIN1252']


def test_get_client_encoding_fallback_when_show_fails(monkeypatch):
    class BrokenConn:
        closed = False

        def cursor(self):
            raise RuntimeError('boom')

    db = ConexionDB()
    db._connection = BrokenConn()
    db._client_encoding = None
    monkeypatch.setattr('app.dao.conexion.Config.DB_CLIENT_ENCODING', 'utf8')

    assert db.get_client_encoding() == 'UTF8'


def test_resolver_encoding_initial_like_behavior():
    db = ConexionDB()
    db._connection = _Conn()
    db._client_encoding = None
    assert db.get_client_encoding() == 'UTF8'
