"""Opt-in HTTP + PostgreSQL tests, restricted to a named synthetic database."""
import os
import uuid

import pytest

from app import create_app
from app.config import Config
from app.dao.conexion import db

pytestmark = pytest.mark.skipif(os.getenv('RUN_SYNTHETIC_PG_TESTS') != '1', reason='requires an explicitly created local synthetic PostgreSQL cluster')


def synthetic_client():
    assert Config.DB_HOST == '127.0.0.1'
    assert Config.DB_NAME.startswith('portfolio_orders_synthetic')
    assert Config.DB_PORT == '55432'
    return create_app({'TESTING': True}).test_client()


def token_for(client, route):
    assert client.get(route).status_code == 200
    with client.session_transaction() as session:
        return session['_csrf']


def test_client_create_read_edit_and_logical_delete_with_postgres():
    client = synthetic_client()
    identifier = 'SYNTH-' + uuid.uuid4().hex[:12]
    token = token_for(client, '/clientes/nuevo')
    data = {'_csrf': token, 'nombre': 'Demo', 'apellido': 'Synthetic', 'cedula': identifier, 'email': 'demo@example.invalid'}
    assert client.post('/clientes/nuevo', data=data).status_code == 302
    with db.get_cursor() as cursor:
        cursor.execute('SELECT id_cliente FROM cliente WHERE cedula=%s', (identifier,))
        ident = cursor.fetchone()['id_cliente']
    assert client.get(f'/clientes/{ident}').status_code == 200
    data['apellido'] = 'Verified'
    assert client.post(f'/clientes/{ident}/editar', data=data).status_code == 302
    with db.get_cursor() as cursor:
        cursor.execute('SELECT apellido FROM cliente WHERE id_cliente=%s', (ident,))
        assert cursor.fetchone()['apellido'] == 'Verified'
    assert client.post(f'/clientes/{ident}/eliminar', data={'_csrf': token}).status_code == 302
    with db.get_cursor() as cursor:
        cursor.execute('SELECT activo FROM cliente WHERE id_cliente=%s', (ident,))
        assert cursor.fetchone()['activo'] is False
    db.cerrar()


def test_service_creation_and_numeric_rejection_with_postgres():
    client = synthetic_client()
    token = token_for(client, '/servicios/nuevo')
    name = 'Synthetic verification ' + uuid.uuid4().hex[:8]
    data = {'_csrf': token, 'nombre_servicio': name, 'descripcion': 'Synthetic test only', 'costo_base': '12.50', 'tiempo_estimado_horas': '2'}
    assert client.post('/servicios/nuevo', data=data).status_code == 302
    with db.get_cursor() as cursor:
        cursor.execute('SELECT id_servicio,costo_base FROM servicio WHERE nombre_servicio=%s', (name,))
        row = cursor.fetchone()
        assert str(row['costo_base']) == '12.50'
    assert client.get(f'/servicios/{row["id_servicio"]}').status_code == 200
    data['nombre_servicio'] += ' invalid'
    data['costo_base'] = 'NaN'
    response = client.post('/servicios/nuevo', data=data)
    assert response.status_code == 200
    assert b'finito' in response.data
    with db.get_cursor() as cursor:
        cursor.execute('SELECT COUNT(*) AS total FROM servicio WHERE nombre_servicio=%s', (data['nombre_servicio'],))
        assert cursor.fetchone()['total'] == 0
    db.cerrar()
