# app/config.py
"""
Configuración centralizada de la aplicación
"""
import os
from pathlib import Path
import secrets
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / '.env')


class Config:
    # Base de datos PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'servicios')
    DB_USER = os.getenv('DB_USER', 'usuario')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_CLIENT_ENCODING = os.getenv('DB_CLIENT_ENCODING', 'UTF8')
    DB_FALLBACK_ENCODING = os.getenv('DB_FALLBACK_ENCODING', 'LATIN1')

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_urlsafe(32)
    DEBUG = os.getenv('FLASK_DEBUG', '').lower() in ('1', 'true')
    MAX_CONTENT_LENGTH = 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    TRUSTED_HOSTS = ['localhost', '127.0.0.1']
