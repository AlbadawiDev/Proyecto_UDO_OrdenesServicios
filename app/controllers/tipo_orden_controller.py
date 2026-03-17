# app/controllers/tipo_orden_controller.py
"""
Controlador para la entidad TipoOrden
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.tipo_orden_service import tipo_orden_service

tipo_orden_bp = Blueprint('tipo_orden', __name__)

@tipo_orden_bp.route('/')
def listar_tipos():
    resultado = tipo_orden_service.listar()
    if resultado['exito']:
        return render_template('tipo_orden/listar.html', tipos=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('tipo_orden/listar.html', tipos=[])

@tipo_orden_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_tipo():
    if request.method == 'POST':
        datos = {
            'nombre_tipo': request.form.get('nombre_tipo'),
            'descripcion': request.form.get('descripcion'),
            'requiere_aprobacion': request.form.get('requiere_aprobacion') == 'on'
        }
        resultado = tipo_orden_service.crear(datos)
        if resultado['exito']:
            flash('Tipo de orden creado exitosamente', 'success')
            return redirect(url_for('tipo_orden.listar_tipos'))
        else:
            flash(resultado['mensaje'], 'error')
    return render_template('tipo_orden/crear.html')

@tipo_orden_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_tipo(id):
    if request.method == 'POST':
        datos = {
            'nombre_tipo': request.form.get('nombre_tipo'),
            'descripcion': request.form.get('descripcion'),
            'requiere_aprobacion': request.form.get('requiere_aprobacion') == 'on'
        }
        resultado = tipo_orden_service.actualizar(id, datos)
        if resultado['exito']:
            flash('Tipo de orden actualizado exitosamente', 'success')
            return redirect(url_for('tipo_orden.listar_tipos'))
        else:
            flash(resultado['mensaje'], 'error')
    
    resultado = tipo_orden_service.consultar(id)
    if resultado['exito']:
        return render_template('tipo_orden/editar.html', tipo=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('tipo_orden.listar_tipos'))

@tipo_orden_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_tipo(id):
    resultado = tipo_orden_service.eliminar(id)
    if resultado['exito']:
        flash('Tipo de orden eliminado exitosamente', 'success')
    else:
        flash(resultado['mensaje'], 'error')
    return redirect(url_for('tipo_orden.listar_tipos'))