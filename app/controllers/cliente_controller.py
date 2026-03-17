# app/controllers/cliente_controller.py
"""
Controlador para la entidad Cliente
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.cliente_service import cliente_service

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/')
def listar_clientes():
    resultado = cliente_service.listar()
    if resultado['exito']:
        return render_template('cliente/listar.html', clientes=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('cliente/listar.html', clientes=[])

@cliente_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'cedula': request.form.get('cedula'),
            'telefono': request.form.get('telefono'),
            'email': request.form.get('email'),
            'direccion': request.form.get('direccion')
        }
        resultado = cliente_service.crear(datos)
        if resultado['exito']:
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        else:
            flash(resultado['mensaje'], 'error')
    return render_template('cliente/crear.html')

@cliente_bp.route('/<int:id>')
def ver_cliente(id):
    resultado = cliente_service.consultar(id)
    if resultado['exito']:
        return render_template('cliente/ver.html', cliente=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('cliente.listar_clientes'))

@cliente_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'cedula': request.form.get('cedula'),
            'telefono': request.form.get('telefono'),
            'email': request.form.get('email'),
            'direccion': request.form.get('direccion')
        }
        resultado = cliente_service.actualizar(id, datos)
        if resultado['exito']:
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        else:
            flash(resultado['mensaje'], 'error')
    
    resultado = cliente_service.consultar(id)
    if resultado['exito']:
        return render_template('cliente/editar.html', cliente=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('cliente.listar_clientes'))

@cliente_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    resultado = cliente_service.eliminar(id)
    if resultado['exito']:
        flash('Cliente eliminado exitosamente', 'success')
    else:
        flash(resultado['mensaje'], 'error')
    return redirect(url_for('cliente.listar_clientes'))

@cliente_bp.route('/api/buscar')
def api_buscar():
    criterio = request.args.get('criterio', 'nombre')
    valor = request.args.get('valor', '')
    if criterio == 'cedula':
        resultado = cliente_service.buscar_por_cedula(valor)
    else:
        resultado = cliente_service.buscar(criterio, valor)
    return jsonify(resultado)