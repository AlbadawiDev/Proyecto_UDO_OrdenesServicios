# app/controllers/prioridad_controller.py
"""
Controlador para la entidad Prioridad
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.prioridad_service import prioridad_service

prioridad_bp = Blueprint('prioridad', __name__)

@prioridad_bp.route('/')
def listar_prioridades():
    resultado = prioridad_service.listar()
    if resultado['exito']:
        return render_template('prioridad/listar.html', prioridades=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('prioridad/listar.html', prioridades=[])

@prioridad_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_prioridad():
    if request.method == 'POST':
        datos = {
            'nombre_prioridad': request.form.get('nombre_prioridad'),
            'nivel': int(request.form.get('nivel', 1)),
            'tiempo_respuesta_horas': int(request.form.get('tiempo_respuesta_horas')) if request.form.get('tiempo_respuesta_horas') else None,
            'color_hex': request.form.get('color_hex', '#FF0000')
        }
        resultado = prioridad_service.crear(datos)
        if resultado['exito']:
            flash('Prioridad creada exitosamente', 'success')
            return redirect(url_for('prioridad.listar_prioridades'))
        else:
            flash(resultado['mensaje'], 'error')
    return render_template('prioridad/crear.html')

@prioridad_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_prioridad(id):
    if request.method == 'POST':
        datos = {
            'nombre_prioridad': request.form.get('nombre_prioridad'),
            'nivel': int(request.form.get('nivel', 1)),
            'tiempo_respuesta_horas': int(request.form.get('tiempo_respuesta_horas')) if request.form.get('tiempo_respuesta_horas') else None,
            'color_hex': request.form.get('color_hex', '#FF0000')
        }
        resultado = prioridad_service.actualizar(id, datos)
        if resultado['exito']:
            flash('Prioridad actualizada exitosamente', 'success')
            return redirect(url_for('prioridad.listar_prioridades'))
        else:
            flash(resultado['mensaje'], 'error')
    
    resultado = prioridad_service.consultar(id)
    if resultado['exito']:
        return render_template('prioridad/editar.html', prioridad=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('prioridad.listar_prioridades'))

@prioridad_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_prioridad(id):
    resultado = prioridad_service.eliminar(id)
    if resultado['exito']:
        flash('Prioridad eliminada exitosamente', 'success')
    else:
        flash(resultado['mensaje'], 'error')
    return redirect(url_for('prioridad.listar_prioridades'))