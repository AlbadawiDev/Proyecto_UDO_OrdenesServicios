# app/controllers/tecnico_controller.py
"""
Controlador para la entidad Técnico
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.tecnico_service import tecnico_service

tecnico_bp = Blueprint('tecnico', __name__)

@tecnico_bp.route('/')
def listar_tecnicos():
    resultado = tecnico_service.listar()
    if resultado['exito']:
        return render_template('tecnico/listar.html', tecnicos=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return render_template('tecnico/listar.html', tecnicos=[])

@tecnico_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_tecnico():
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'cedula': request.form.get('cedula'),
            'especialidad': request.form.get('especialidad'),
            'telefono': request.form.get('telefono'),
            'email': request.form.get('email'),
            'fecha_contratacion': request.form.get('fecha_contratacion')
        }
        resultado = tecnico_service.crear(datos)
        if resultado['exito']:
            flash('Técnico creado exitosamente', 'success')
            return redirect(url_for('tecnico.listar_tecnicos'))
        else:
            flash(resultado['mensaje'], 'error')
    return render_template('tecnico/crear.html')

@tecnico_bp.route('/<int:id>')
def ver_tecnico(id):
    resultado = tecnico_service.consultar(id)
    if resultado['exito']:
        return render_template('tecnico/ver.html', tecnico=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('tecnico.listar_tecnicos'))

@tecnico_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_tecnico(id):
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'cedula': request.form.get('cedula'),
            'especialidad': request.form.get('especialidad'),
            'telefono': request.form.get('telefono'),
            'email': request.form.get('email'),
            'fecha_contratacion': request.form.get('fecha_contratacion')
        }
        resultado = tecnico_service.actualizar(id, datos)
        if resultado['exito']:
            flash('Técnico actualizado exitosamente', 'success')
            return redirect(url_for('tecnico.listar_tecnicos'))
        else:
            flash(resultado['mensaje'], 'error')
    
    resultado = tecnico_service.consultar(id)
    if resultado['exito']:
        return render_template('tecnico/editar.html', tecnico=resultado['data'])
    flash(resultado['mensaje'], 'error')
    return redirect(url_for('tecnico.listar_tecnicos'))

@tecnico_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_tecnico(id):
    resultado = tecnico_service.eliminar(id)
    if resultado['exito']:
        flash('Técnico eliminado exitosamente', 'success')
    else:
        flash(resultado['mensaje'], 'error')
    return redirect(url_for('tecnico.listar_tecnicos'))

@tecnico_bp.route('/api/buscar')
def api_buscar():
    criterio = request.args.get('criterio', 'nombre')
    valor = request.args.get('valor', '')
    resultado = tecnico_service.buscar(criterio, valor)
    return jsonify(resultado)