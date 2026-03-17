# app/controllers/servicio_controller.py
"""
Controlador para la entidad Servicio
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.servicio_service import servicio_service

servicio_bp = Blueprint('servicio', __name__)

@servicio_bp.route('/')
def listar_servicios():
    resultado = servicio_service.listar()
    if resultado['exito']:
        return render_template('servicio/listar.html', servicios=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('servicio/listar.html', servicios=[])

@servicio_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_servicio():
    if request.method == 'POST':
        datos = {
            'nombre_servicio': request.form.get('nombre_servicio'),
            'descripcion': request.form.get('descripcion'),
            'costo_base': float(request.form.get('costo_base')) if request.form.get('costo_base') else None,
            'tiempo_estimado_horas': int(request.form.get('tiempo_estimado_horas')) if request.form.get('tiempo_estimado_horas') else None
        }
        resultado = servicio_service.crear(datos)
        if resultado['exito']:
            flash('Servicio creado exitosamente', 'success')
            return redirect(url_for('servicio.listar_servicios'))
        else:
            flash(resultado['mensaje'], 'error')
    return render_template('servicio/crear.html')

@servicio_bp.route('/<int:id>')
def ver_servicio(id):
    resultado = servicio_service.consultar(id)
    if resultado['exito']:
        return render_template('servicio/ver.html', servicio=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('servicio.listar_servicios'))

@servicio_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_servicio(id):
    if request.method == 'POST':
        datos = {
            'nombre_servicio': request.form.get('nombre_servicio'),
            'descripcion': request.form.get('descripcion'),
            'costo_base': float(request.form.get('costo_base')) if request.form.get('costo_base') else None,
            'tiempo_estimado_horas': int(request.form.get('tiempo_estimado_horas')) if request.form.get('tiempo_estimado_horas') else None
        }
        resultado = servicio_service.actualizar(id, datos)
        if resultado['exito']:
            flash('Servicio actualizado exitosamente', 'success')
            return redirect(url_for('servicio.listar_servicios'))
        else:
            flash(resultado['mensaje'], 'error')
    
    resultado = servicio_service.consultar(id)
    if resultado['exito']:
        return render_template('servicio/editar.html', servicio=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('servicio.listar_servicios'))

@servicio_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_servicio(id):
    resultado = servicio_service.eliminar(id)
    if resultado['exito']:
        flash('Servicio eliminado exitosamente', 'success')
    else:
        flash(resultado['mensaje'], 'error')
    return redirect(url_for('servicio.listar_servicios'))