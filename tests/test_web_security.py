import threading
from unittest.mock import Mock

import pytest

from app import create_app
from app.dao.base_dao import BaseDAO
from app.dao.conexion import db
from app.services.base_service import BaseService
from app.utils.input_parsers import parse_float


@pytest.fixture
def client():
    return create_app({'TESTING': True, 'SECRET_KEY': 'synthetic-test-secret'}).test_client()


def test_dashboard_renders_without_database(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'no-store' in response.headers['Cache-Control'].encode()
    assert response.headers['X-Content-Type-Options'] == 'nosniff'


def test_form_renders_csrf_and_post_without_it_never_calls_service(client, monkeypatch):
    create = Mock(return_value={'exito': True})
    monkeypatch.setattr('app.controllers.cliente_controller.cliente_service.crear', create)
    response = client.get('/clientes/nuevo')
    assert b'name="_csrf"' in response.data
    response = client.post('/clientes/nuevo', data={'nombre': 'Demo'})
    assert response.status_code == 403
    create.assert_not_called()


def test_valid_csrf_allows_mocked_creation(client, monkeypatch):
    create = Mock(return_value={'exito': True})
    monkeypatch.setattr('app.controllers.cliente_controller.cliente_service.crear', create)
    client.get('/clientes/nuevo')
    with client.session_transaction() as session:
        token = session['_csrf']
    response = client.post('/clientes/nuevo', data={'_csrf': token, 'nombre': 'Demo', 'apellido': 'Synthetic', 'cedula': 'TEST-001'})
    assert response.status_code == 302
    create.assert_called_once()
    assert '_csrf' not in create.call_args.args[0]


def test_invalid_host_is_rejected(client):
    assert client.get('/', headers={'Host': 'attacker.example'}).status_code == 400


@pytest.mark.parametrize('value', ['nan', 'NaN', 'inf', '-inf', '1e999'])
def test_nonfinite_costs_are_rejected(value):
    with pytest.raises(ValueError, match='finito'):
        parse_float(value, 'costo', required=True, minimum=0)


class DAO(BaseDAO):
    tabla = 'cliente'
    primary_key = 'id_cliente'

    def mapear_a_objeto(self, row):
        return row


@pytest.mark.parametrize('operation', ['insertar', 'actualizar'])
def test_malicious_write_columns_never_reach_database(operation, monkeypatch):
    cursor = Mock()
    monkeypatch.setattr('app.dao.base_dao.db.get_cursor', cursor)
    with pytest.raises(ValueError, match='SQL'):
        if operation == 'insertar':
            DAO().insertar({'nombre) VALUES (1); DROP TABLE cliente; --': 'Synthetic'})
        else:
            DAO().actualizar(1, {'nombre=1; --': 'Synthetic'})
    cursor.assert_not_called()


def test_prevalidation_database_failure_returns_safe_service_result():
    dao = Mock()
    dao.buscar_por_id.side_effect = RuntimeError('synthetic-private-db-detail')
    result = BaseService(dao).actualizar(1, {})
    assert result['exito'] is False
    assert 'synthetic-private-db-detail' not in result['mensaje']


def test_connections_are_isolated_between_threads():
    previous = db._connection
    marker = object()
    db._connection = marker
    observed = []

    def in_worker():
        observed.append(db._connection)
        db._connection = object()

    thread = threading.Thread(target=in_worker)
    try:
        thread.start()
        thread.join(timeout=2)
        assert observed == [None]
        assert db._connection is marker
    finally:
        db._connection = previous
