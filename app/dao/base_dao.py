"""Clase base abstracta para todos los DAOs."""
from abc import ABC, abstractmethod
import logging
import re

from app.dao.conexion import db

logger = logging.getLogger(__name__)
_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_ENCODING_ERROR_MARKERS = (
    "codec can't decode",
    "invalid continuation byte",
    "invalid start byte",
    "character with byte sequence",
)


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

    def _es_error_encoding(self, exc):
        if isinstance(exc, UnicodeDecodeError):
            return True

        visited = set()
        current = exc
        while current and id(current) not in visited:
            visited.add(id(current))
            if isinstance(current, UnicodeDecodeError):
                return True
            message = str(current).lower()
            if any(marker in message for marker in _ENCODING_ERROR_MARKERS):
                return True
            current = current.__cause__ or current.__context__
        return False

    def _execute_fetch(self, query, params=(), fetch_one=False):
        """Ejecuta consulta SELECT con fallback de encodings antes de propagar error."""
        encodings = db.obtener_encodings_preferidos()
        original_encoding = db.get_client_encoding()
        if original_encoding in encodings:
            encodings = [original_encoding] + [e for e in encodings if e != original_encoding]

        last_exc = None
        for idx, encoding in enumerate(encodings):
            cursor = None
            try:
                if db.get_client_encoding() != encoding:
                    db.set_client_encoding(encoding)
                cursor = db.get_cursor()
                cursor.execute(query, params)
                result = cursor.fetchone() if fetch_one else cursor.fetchall()
                if encoding != original_encoding:
                    logger.info('Lectura recuperada con encoding %s; restaurando %s', encoding, original_encoding)
                    db.set_client_encoding(original_encoding)
                return result
            except Exception as exc:
                if not self._es_error_encoding(exc):
                    raise

                last_exc = exc
                db.rollback()
                logger.warning(
                    'Error de decoding en lectura (%s). Intento %s/%s con encoding %s',
                    exc,
                    idx + 1,
                    len(encodings),
                    encoding,
                )
                if idx + 1 < len(encodings):
                    try:
                        db.reconnect(preferred_encoding=encodings[idx + 1])
                    except Exception:
                        logger.exception('Falló reconexión para encoding %s', encodings[idx + 1])
                continue
            finally:
                if cursor:
                    cursor.close()

        if original_encoding != db.get_client_encoding():
            db.set_client_encoding(original_encoding)
        raise last_exc

    def _query_rows(self, query, params=()):
        return self._execute_fetch(query, params, fetch_one=False)

    def _query_row(self, query, params=()):
        return self._execute_fetch(query, params, fetch_one=True)

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
        fila = self._query_row(query, (id_valor,))
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

        filas = self._query_rows(query, tuple(params))
        return [self.mapear_a_objeto(fila) for fila in filas]

    def buscar_por_criterio(self, columna, valor):
        self._validar_identificador(columna)
        query = f"SELECT * FROM {self.tabla} WHERE {columna} = %s AND activo = TRUE"
        filas = self._query_rows(query, (valor,))
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
