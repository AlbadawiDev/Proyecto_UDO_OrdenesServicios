"""Clase base abstracta para todos los DAOs."""
from abc import ABC, abstractmethod
import logging
import re
import psycopg2

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
        if not isinstance(identificador, str) or not _IDENTIFIER_PATTERN.fullmatch(identificador):
            raise ValueError(f"Identificador SQL inválido: {identificador}")

    @staticmethod
    def _es_error_encoding(exc):
        """Recognize decoding wrappers without retrying ordinary SQL failures."""
        pending, visited = [exc], set()
        while pending:
            current = pending.pop()
            if current is None or id(current) in visited:
                continue
            visited.add(id(current))
            if isinstance(current, UnicodeDecodeError):
                return True
            if not isinstance(current, psycopg2.Error):
                message = str(current).lower()
                if ("utf-8" in message and "codec can't decode byte" in message
                        and any(reason in message for reason in (
                            'invalid start byte', 'invalid continuation byte', 'unexpected end of data'))):
                    return True
            pending.extend((current.__cause__, current.__context__))
        return False

    def _execute_fetch(self, query, params=(), fetch_one=False):
        cursor = None
        restore_encoding = False
        original_encoding = None
        try:
            cursor = db.get_cursor()
            original_encoding = db.get_client_encoding()
            try:
                cursor.execute(query, params)
                return cursor.fetchone() if fetch_one else cursor.fetchall()
            except Exception as exc:
                fallback = Config.DB_FALLBACK_ENCODING
                if not self._es_error_encoding(exc) or fallback.upper() == original_encoding.upper():
                    raise
                logger.info("Error de decoding en lectura; un retry con %s", fallback)
                db.rollback()
                cursor.close()
                cursor = None
                restore_encoding = True
                db.set_client_encoding(fallback)
                try:
                    cursor = db.get_cursor()
                    cursor.execute(query, params)
                    return cursor.fetchone() if fetch_one else cursor.fetchall()
                except Exception:
                    db.rollback()
                    raise
        finally:
            try:
                if cursor:
                    cursor.close()
            finally:
                if restore_encoding:
                    try:
                        db.set_client_encoding(original_encoding)
                    except Exception:
                        db.cerrar()
                        raise

    def insertar(self, datos: dict) -> int:
        self._validar_identificador(self.tabla)
        self._validar_identificador(self.primary_key)
        for columna in datos:
            self._validar_identificador(columna)
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
        self._validar_identificador(self.tabla)
        self._validar_identificador(self.primary_key)
        for columna in datos:
            self._validar_identificador(columna)
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
