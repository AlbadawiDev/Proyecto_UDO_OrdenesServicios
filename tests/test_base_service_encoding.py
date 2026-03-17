from app.services.base_service import BaseService


class _DAO:
    def listar_todos(self, limite=None, offset=None):
        raise UnicodeDecodeError('utf-8', b'\xf3', 0, 1, 'invalid continuation byte')


class _Service(BaseService):
    def __init__(self):
        super().__init__(_DAO())


def test_listar_no_expone_error_unicode():
    service = _Service()
    resultado = service.listar()
    assert resultado['exito'] is False
    assert 'utf-8' not in resultado['mensaje'].lower()
    assert 'problema temporal' in resultado['mensaje'].lower()
