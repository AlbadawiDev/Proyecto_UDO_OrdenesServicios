# app/dao/conexion.py
"""Capa de conexión y recuperación de encoding para PostgreSQL."""
import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import Config

logger = logging.getLogger(__name__)


class ConexionDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
            cls._instance._client_encoding = None
        return cls._instance

    @staticmethod
    def _normalizar_encoding(encoding):
        return (encoding or 'UTF8').strip().upper()

    def obtener_encodings_preferidos(self):
        encodings = [
            self._normalizar_encoding(Config.DB_CLIENT_ENCODING),
            self._normalizar_encoding(Config.DB_FALLBACK_ENCODING),
        ]
        extras = getattr(Config, 'DB_EXTRA_FALLBACK_ENCODINGS', '') or ''
        for extra in extras.split(','):
            extra_norm = self._normalizar_encoding(extra)
            if extra_norm and extra_norm not in encodings:
                encodings.append(extra_norm)
        return encodings

    def conectar(self):
        try:
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                )
                self._connection.autocommit = False
                self.set_client_encoding(self._normalizar_encoding(Config.DB_CLIENT_ENCODING))
                logger.info('Conexión a PostgreSQL establecida')
            return self._connection
        except psycopg2.Error as exc:
            logger.error('Error de conexión: %s', exc)
            raise

    def reconnect(self, preferred_encoding=None):
        self.cerrar()
        conn = self.conectar()
        if preferred_encoding:
            self.set_client_encoding(preferred_encoding)
        return conn

    def set_client_encoding(self, encoding):
        conn = self.conectar()
        normalized = self._normalizar_encoding(encoding)
        conn.set_client_encoding(normalized)
        self._client_encoding = normalized
        logger.info('client_encoding configurado a %s', normalized)

    def get_client_encoding(self):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SHOW client_encoding')
                encoding = (cursor.fetchone() or ['UTF8'])[0]
                self._client_encoding = self._normalizar_encoding(encoding)
        except Exception:
            if not self._client_encoding:
                self._client_encoding = self._normalizar_encoding(Config.DB_CLIENT_ENCODING)
        return self._client_encoding

    def cerrar(self):
        if self._connection and not self._connection.closed:
            self._connection.close()
            logger.info('Conexión cerrada')

    def get_cursor(self, dictionary=True):
        conn = self.conectar()

        if conn.get_transaction_status() == psycopg2.extensions.TRANSACTION_STATUS_INERROR:
            logger.warning('Transacción abortada detectada, ejecutando ROLLBACK')
            conn.rollback()

        if dictionary:
            return conn.cursor(cursor_factory=RealDictCursor)
        return conn.cursor()

    def commit(self):
        if self._connection:
            self._connection.commit()

    def rollback(self):
        if self._connection:
            self._connection.rollback()
            logger.info('Rollback ejecutado')


db = ConexionDB()
