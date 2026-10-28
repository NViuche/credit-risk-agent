"""Acceso de solo lectura a Supabase (PostgreSQL)."""
import psycopg2
import psycopg2.extras

from config import settings


class ErrorDatos(Exception):
    """Fallo de conexión o de consulta, con un mensaje apto para mostrar al usuario."""


def consultar(sql: str, parametros: tuple = ()) -> list[dict]:
    """Ejecuta una consulta en una sesión de solo lectura y devuelve filas como diccionarios."""
    if not settings.DATABASE_URL:
        raise ErrorDatos("Falta DATABASE_URL en el archivo .env.")
    try:
        with psycopg2.connect(settings.DATABASE_URL, connect_timeout=10) as conn:
            conn.set_session(readonly=True)
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, parametros)
                return [dict(fila) for fila in cur.fetchall()]
    except psycopg2.Error as e:
        raise ErrorDatos(f"Error al consultar Supabase: {e.__class__.__name__}: {e}".strip()) from e
