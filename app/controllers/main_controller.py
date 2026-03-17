# app/controllers/main_controller.py
"""
Controlador principal - Dashboard
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal con dashboard"""
    return render_template('index.html')