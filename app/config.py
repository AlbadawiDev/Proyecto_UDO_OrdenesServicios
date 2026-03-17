# app/config.py
"""
Configuración centralizada de la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Base de datos PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'servicios')
    DB_USER = os.getenv('DB_USER', 'usuario')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '12345678')
    DB_CLIENT_ENCODING = os.getenv('DB_CLIENT_ENCODING', 'UTF8')
    DB_FALLBACK_ENCODING = os.getenv('DB_FALLBACK_ENCODING', 'LATIN1')
    DB_EXTRA_FALLBACK_ENCODINGS = os.getenv('DB_EXTRA_FALLBACK_ENCODINGS', 'WIN1252')

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', '12345678')
    DEBUG = True
