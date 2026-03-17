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
    def cursor(self):
        return _Cursor()


def test_resolver_encoding_inicial_usa_config_por_defecto():
    db = ConexionDB()
    encoding = db._resolver_encoding_inicial(_Conn())
    assert encoding == 'UTF8'
