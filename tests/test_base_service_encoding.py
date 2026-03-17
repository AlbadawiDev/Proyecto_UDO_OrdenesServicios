from app.services.base_service import BaseService


class _DAO:
    def listar_todos(self, limite=None, offset=None):
        raise UnicodeDecodeError('utf-8', b'\xf3', 0, 1, 'invalid continuation byte')


<<<<<<< HEAD
class _DAOMessage:
    def listar_todos(self, limite=None, offset=None):
        raise RuntimeError("'utf-8' codec can't decode byte 0xf3 in position 85: invalid continuation byte")


class _Service(BaseService):
    def __init__(self, dao):
        super().__init__(dao)


def test_listar_no_expone_error_unicode():
    service = _Service(_DAO())
    resultado = service.listar()
    assert resultado['exito'] is False
    assert 'utf-8' not in resultado['mensaje'].lower()
    assert 'problema temporal' in resultado['mensaje'].lower()


def test_listar_no_expone_error_unicode_en_mensaje_generico():
    service = _Service(_DAOMessage())
=======
class _Service(BaseService):
    def __init__(self):
        super().__init__(_DAO())


def test_listar_no_expone_error_unicode():
    service = _Service()
>>>>>>> origin/codex/review-and-complete-flask-service-order-system
    resultado = service.listar()
    assert resultado['exito'] is False
    assert 'utf-8' not in resultado['mensaje'].lower()
    assert 'problema temporal' in resultado['mensaje'].lower()
