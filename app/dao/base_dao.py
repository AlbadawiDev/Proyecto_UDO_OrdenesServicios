"""Clase base abstracta para todos los DAOs."""
from abc import ABC, abstractmethod
import logging
import re

from app.config import Config
from app.dao.conexion import db

logger = logging.getLogger(__name__)
_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


class BaseDAO(ABC):
    @property
    @abstractmethod
    def tabla(self):
        pass

    @property
    @abstractmethod
    def primary_key(self):
        pass

    @abstractmethod
    def mapear_a_objeto(self, fila):
        pass

    def _validar_identificador(self, identificador):
        if not _IDENTIFIER_PATTERN.match(identificador):
            raise ValueError(f"Identificador SQL inválido: {identificador}")

    def _execute_fetch(self, query, params=(), fetch_one=False):
        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, params)
            return cursor.fetchone() if fetch_one else cursor.fetchall()
        except UnicodeDecodeError as exc:
            fallback = Config.DB_FALLBACK_ENCODING
            logger.info("UnicodeDecodeError leyendo filas (%s). Retry con %s", exc, fallback)
            db.rollback()
            db.set_client_encoding(fallback)
            if cursor:
                cursor.close()
            cursor = db.get_cursor()
            cursor.execute(query, params)
            return cursor.fetchone() if fetch_one else cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def insertar(self, datos: dict) -> int:
        columnas = list(datos.keys())
        valores = list(datos.values())
        placeholders = ", ".join(["%s"] * len(valores))
        cols_str = ", ".join(columnas)
        query = f"""
            INSERT INTO {self.tabla} ({cols_str})
            VALUES ({placeholders})
            RETURNING {self.primary_key}
        """

        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, valores)
            fila = cursor.fetchone()
            id_generado = fila[self.primary_key] if fila else None
            db.commit()
            return id_generado
        except Exception as e:
            db.rollback()
            logger.error("Error insertando en %s: %s", self.tabla, e)
            raise
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_valor):
        query = f"SELECT * FROM {self.tabla} WHERE {self.primary_key} = %s AND activo = TRUE"
        fila = self._execute_fetch(query, (id_valor,), fetch_one=True)
        return self.mapear_a_objeto(fila) if fila else None

    def listar_todos(self, limite=None, offset=None):
        query = f"SELECT * FROM {self.tabla} WHERE activo = TRUE ORDER BY {self.primary_key}"
        params = []
        if limite is not None:
            query += " LIMIT %s"
            params.append(limite)
        if offset is not None:
            query += " OFFSET %s"
            params.append(offset)

        filas = self._execute_fetch(query, tuple(params), fetch_one=False)
        return [self.mapear_a_objeto(fila) for fila in filas]

    def buscar_por_criterio(self, columna, valor):
        self._validar_identificador(columna)
        query = f"SELECT * FROM {self.tabla} WHERE {columna} = %s AND activo = TRUE"
        filas = self._execute_fetch(query, (valor,), fetch_one=False)
        return [self.mapear_a_objeto(fila) for fila in filas]

    def actualizar(self, id_valor, datos: dict):
        if not datos:
            return False
        campos = [f"{k} = %s" for k in datos.keys()]
        valores = list(datos.values())
        valores.append(id_valor)
        query = f"""
            UPDATE {self.tabla}
            SET {", ".join(campos)}
            WHERE {self.primary_key} = %s AND activo = TRUE
        """

        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, valores)
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            logger.error("Error actualizando %s: %s", self.tabla, e)
            raise
        finally:
            if cursor:
                cursor.close()

    def eliminar_logico(self, id_valor):
        query = f"UPDATE {self.tabla} SET activo = FALSE WHERE {self.primary_key} = %s"
        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, (id_valor,))
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            logger.error("Error eliminando %s: %s", self.tabla, e)
            raise
        finally:
            if cursor:
                cursor.close()

    def eliminar_fisico(self, id_valor):
        query = f"DELETE FROM {self.tabla} WHERE {self.primary_key} = %s"
        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, (id_valor,))
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            logger.error("Error eliminando físico %s: %s", self.tabla, e)
            raise
        finally:
            if cursor:
                cursor.close()
