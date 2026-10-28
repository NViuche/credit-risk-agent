"""Configuración central: rutas del proyecto y variables de entorno (.env)."""
import os
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
CARPETA_SKILL = RAIZ / "skills" / "credit-risk"

load_dotenv(RAIZ / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

# Límite de filas por análisis: protege la base de datos y mantiene el informe legible.
MAX_FILAS = 500
