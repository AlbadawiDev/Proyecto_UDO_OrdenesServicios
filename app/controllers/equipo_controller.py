# app/controllers/equipo_controller.py
"""
Controlador para la entidad Equipo
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.equipo_service import equipo_service
from app.services.cliente_service import cliente_service

equipo_bp = Blueprint('equipo', __name__)

@equipo_bp.route('/')
def listar_equipos():
    resultado = equipo_service.listar()
    if resultado['exito']:
        return render_template('equipo/listar.html', equipos=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('equipo/listar.html', equipos=[])

@equipo_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_equipo():
    if request.method == 'POST':
        datos = {
            'nombre_equipo': request.form.get('nombre_equipo'),
            'tipo': request.form.get('tipo'),
            'marca': request.form.get('marca'),
            'modelo': request.form.get('modelo'),
            'numero_serie': request.form.get('numero_serie'),
            'id_cliente': int(request.form.get('id_cliente')) if request.form.get('id_cliente') else None
        }
        resultado = equipo_service.crear(datos)
        if resultado['exito']:
            flash('Equipo registrado exitosamente', 'success')
            return redirect(url_for('equipo.listar_equipos'))
        else:
            flash(resultado['mensaje'], 'error')
    
    # Cargar clientes para el select
    clientes_result = cliente_service.listar()
    clientes = clientes_result['data'] if clientes_result['exito'] else []
    return render_template('equipo/crear.html', clientes=clientes)

@equipo_bp.route('/<int:id>')
def ver_equipo(id):
    resultado = equipo_service.consultar(id)
    if resultado['exito']:
        return render_template('equipo/ver.html', equipo=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('equipo.listar_equipos'))

@equipo_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_equipo(id):
    if request.method == 'POST':
        datos = {
            'nombre_equipo': request.form.get('nombre_equipo'),
            'tipo': request.form.get('tipo'),
            'marca': request.form.get('marca'),
            'modelo': request.form.get('modelo'),
            'numero_serie': request.form.get('numero_serie'),
            'id_cliente': int(request.form.get('id_cliente')) if request.form.get('id_cliente') else None
        }
        resultado = equipo_service.actualizar(id, datos)
        if resultado['exito']:
            flash('Equipo actualizado exitosamente', 'success')
            return redirect(url_for('equipo.listar_equipos'))
        else:
            flash(resultado['mensaje'], 'error')
    
    resultado = equipo_service.consultar(id)
    clientes_result = cliente_service.listar()
    clientes = clientes_result['data'] if clientes_result['exito'] else []
    
    if resultado['exito']:
        return render_template('equipo/editar.html', equipo=resultado['data'], clientes=clientes)
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('equipo.listar_equipos'))

@equipo_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_equipo(id):
    resultado = equipo_service.eliminar(id)
    if resultado['exito']:
        flash('Equipo eliminado exitosamente', 'success')
    else:
        flash(resultado['mensaje'], 'error')
    return redirect(url_for('equipo.listar_equipos'))

@equipo_bp.route('/cliente/<int:id_cliente>')
def listar_por_cliente(id_cliente):
    resultado = equipo_service.listar_por_cliente(id_cliente)
    return jsonify(resultado)