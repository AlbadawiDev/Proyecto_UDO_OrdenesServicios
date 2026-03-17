# app/controllers/estatus_orden_controller.py
"""Controlador para la entidad EstatusOrden."""
from flask import Blueprint, render_template, redirect, request, url_for, flash

from app.services.estatus_orden_service import estatus_orden_service
from app.utils.input_parsers import parse_int

estatus_orden_bp = Blueprint('estatus_orden', __name__)


@estatus_orden_bp.route('/')
def listar_estatus():
    resultado = estatus_orden_service.listar()
    if resultado['exito']:
        return render_template('estatus_orden/listar.html', estatus_list=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('estatus_orden/listar.html', estatus_list=[])


@estatus_orden_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_estatus():
    if request.method == 'POST':
        try:
            datos = {
                'nombre_estatus': request.form.get('nombre_estatus'),
                'descripcion': request.form.get('descripcion'),
                'color_hex': request.form.get('color_hex', '#000000'),
                'orden_secuencial': parse_int(request.form.get('orden_secuencial'), 'orden secuencial', required=True, minimum=0),
            }
            resultado = estatus_orden_service.crear(datos)
            if resultado['exito']:
                flash('Estatus creado exitosamente', 'success')
                return redirect(url_for('estatus_orden.listar_estatus'))
            flash(resultado['mensaje'], 'error')
        except ValueError as exc:
            flash(str(exc), 'error')
    return render_template('estatus_orden/crear.html')


@estatus_orden_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_estatus(id):
    if request.method == 'POST':
        try:
            datos = {
                'nombre_estatus': request.form.get('nombre_estatus'),
                'descripcion': request.form.get('descripcion'),
                'color_hex': request.form.get('color_hex', '#000000'),
                'orden_secuencial': parse_int(request.form.get('orden_secuencial'), 'orden secuencial', required=True, minimum=0),
            }
            resultado = estatus_orden_service.actualizar(id, datos)
            if resultado['exito']:
                flash('Estatus actualizado exitosamente', 'success')
                return redirect(url_for('estatus_orden.listar_estatus'))
            flash(resultado['mensaje'], 'error')
        except ValueError as exc:
            flash(str(exc), 'error')

    resultado = estatus_orden_service.consultar(id)
    if resultado['exito']:
        return render_template('estatus_orden/editar.html', estatus=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('estatus_orden.listar_estatus'))


@estatus_orden_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_estatus(id):
    resultado = estatus_orden_service.eliminar(id)
    flash('Estatus eliminado exitosamente' if resultado['exito'] else resultado['mensaje'], 'success' if resultado['exito'] else 'error')
    return redirect(url_for('estatus_orden.listar_estatus'))
