"""
Clase base abstracta para todos los DAOs.
Implementa operaciones CRUD genéricas.
"""
from abc import ABC, abstractmethod
import logging

from app.dao.conexion import db

logger = logging.getLogger(__name__)


class BaseDAO(ABC):
    """
    Clase base para todos los DAOs del sistema.
    Define la interfaz común CRUD.
    """

    @property
    @abstractmethod
    def tabla(self):
        """Nombre de la tabla en la base de datos"""
        pass

    @property
    @abstractmethod
    def primary_key(self):
        """Nombre de la columna clave primaria"""
        pass

    @abstractmethod
    def mapear_a_objeto(self, fila):
        """Convierte una fila de BD a objeto modelo"""
        pass

    def _ejecutar_query(self, query, params=None, fetch=False, fetch_one=False):
        """
        Método helper para ejecutar queries con manejo de transacciones.
        """
        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, params or ())

            if fetch_one:
                return cursor.fetchone()
            if fetch:
                return cursor.fetchall()

            db.commit()
            return cursor.rowcount

        except Exception as e:
            logger.error(f"Error en query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            db.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def insertar(self, datos: dict) -> int:
        """Inserta un nuevo registro en la tabla."""
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
            logger.info(f"Insertado en {self.tabla}: ID {id_generado}")
            return id_generado
        except Exception as e:
            db.rollback()
            logger.error(f"Error insertando en {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_valor):
        """Busca un registro por su ID"""
        query = f"SELECT * FROM {self.tabla} WHERE {self.primary_key} = %s AND activo = TRUE"
        cursor = None

        try:
            cursor = db.get_cursor()
            cursor.execute(query, (id_valor,))
            fila = cursor.fetchone()
            return self.mapear_a_objeto(fila) if fila else None
        except Exception as e:
            logger.error(f"Error buscando en {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self, limite=None, offset=None):
        """Lista todos los registros activos con paginación opcional"""
        query = f"SELECT * FROM {self.tabla} WHERE activo = TRUE ORDER BY {self.primary_key}"
        params = []
        cursor = None

        if limite is not None:
            query += " LIMIT %s"
            params.append(limite)
        if offset is not None:
            query += " OFFSET %s"
            params.append(offset)

        try:
            cursor = db.get_cursor()
            cursor.execute(query, tuple(params))
            filas = cursor.fetchall()
            return [self.mapear_a_objeto(fila) for fila in filas]
        except Exception as e:
            logger.error(f"Error listando {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def buscar_por_criterio(self, columna, valor):
        """Búsqueda genérica por cualquier columna"""
        query = f"SELECT * FROM {self.tabla} WHERE {columna} = %s AND activo = TRUE"
        cursor = None

        try:
            cursor = db.get_cursor()
            cursor.execute(query, (valor,))
            filas = cursor.fetchall()
            return [self.mapear_a_objeto(fila) for fila in filas]
        except Exception as e:
            logger.error(f"Error buscando en {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def actualizar(self, id_valor, datos: dict):
        """Actualiza un registro existente."""
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
            actualizado = cursor.rowcount > 0
            if actualizado:
                logger.info(f"Actualizado {self.tabla} ID {id_valor}")
            return actualizado
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def eliminar_logico(self, id_valor):
        """Eliminación lógica. Cambia activo a FALSE."""
        query = f"""
            UPDATE {self.tabla}
            SET activo = FALSE
            WHERE {self.primary_key} = %s
        """

        cursor = None
        try:
            cursor = db.get_cursor()
            cursor.execute(query, (id_valor,))
            db.commit()
            eliminado = cursor.rowcount > 0
            if eliminado:
                logger.info(f"Eliminado lógico {self.tabla} ID {id_valor}")
            return eliminado
        except Exception as e:
            db.rollback()
            logger.error(f"Error eliminando {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def eliminar_fisico(self, id_valor):
        """Eliminación física permanente."""
        query = f"DELETE FROM {self.tabla} WHERE {self.primary_key} = %s"
        cursor = None

        try:
            cursor = db.get_cursor()
            cursor.execute(query, (id_valor,))
            db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            db.rollback()
            logger.error(f"Error eliminando físico {self.tabla}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()