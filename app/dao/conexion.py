# app/dao/conexion.py
"""
Capa de Persistencia - Módulo de Conexión
Gestiona la conexión a PostgreSQL usando psycopg2
"""
import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConexionDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def _resolver_encoding_inicial(self, conn):
        encoding = (Config.DB_CLIENT_ENCODING or 'UTF8').upper()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW server_encoding")
                server_encoding = (cursor.fetchone() or ['UTF8'])[0]
            logger.info("Encoding servidor PostgreSQL detectado: %s", server_encoding)
        except Exception:
            logger.warning("No se pudo obtener server_encoding. Se usará %s", encoding)
        return encoding

    def conectar(self):
        try:
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD
                )
                self._connection.autocommit = False
                encoding = self._resolver_encoding_inicial(self._connection)
                self.set_client_encoding(encoding)
                logger.info("Conexión a PostgreSQL establecida")
            return self._connection
        except psycopg2.Error as e:
            logger.error(f"Error de conexión: {e}")
            raise

    def set_client_encoding(self, encoding):
        conn = self.conectar()
        conn.set_client_encoding(encoding)
        logger.warning("client_encoding actualizado dinámicamente a %s", encoding)

    def cerrar(self):
        if self._connection and not self._connection.closed:
            self._connection.close()
            logger.info("Conexión cerrada")

    def get_cursor(self, dictionary=True):
        conn = self.conectar()

        if conn.get_transaction_status() == psycopg2.extensions.TRANSACTION_STATUS_INERROR:
            logger.warning("Transacción abortada detectada, haciendo ROLLBACK...")
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
            logger.info("Rollback ejecutado")


db = ConexionDB()
