# app/__init__.py
"""
Inicialización de la aplicación Flask
"""
from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar blueprints (controladores)
    from app.controllers.main_controller import main_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.tecnico_controller import tecnico_bp
    from app.controllers.equipo_controller import equipo_bp
    from app.controllers.servicio_controller import servicio_bp
    from app.controllers.tipo_orden_controller import tipo_orden_bp
    from app.controllers.estatus_orden_controller import estatus_orden_bp
    from app.controllers.prioridad_controller import prioridad_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(cliente_bp, url_prefix='/clientes')
    app.register_blueprint(tecnico_bp, url_prefix='/tecnicos')
    app.register_blueprint(equipo_bp, url_prefix='/equipos')
    app.register_blueprint(servicio_bp, url_prefix='/servicios')
    app.register_blueprint(tipo_orden_bp, url_prefix='/tipos-orden')
    app.register_blueprint(estatus_orden_bp, url_prefix='/estatus-orden')
    app.register_blueprint(prioridad_bp, url_prefix='/prioridades')
    
    return app