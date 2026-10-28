"""Comprueba que el sistema puede consultar la base de datos de Supabase."""
import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
database_url = os.getenv("DATABASE_URL")

if not supabase_url or not supabase_key:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env.")

if not database_url:
    raise RuntimeError("Falta DATABASE_URL en el archivo .env.")

with psycopg2.connect(database_url) as conn:
    # 1. Muestra de datos
    df = pd.read_sql("SELECT * FROM public.credit_risk LIMIT 10;", conn)
    print(df)

    # 2. Verificación: debe dar 32581 filas y 21.82 % de impago
    kpi = pd.read_sql(
        """
        SELECT count(*) AS filas,
               round(avg(loan_status) * 100, 2) AS tasa_impago_pct
        FROM public.credit_risk;
        """,
        conn,
    )
    print(kpi)

supabase = create_client(supabase_url, supabase_key)
api_result = (
    supabase.table("credit_risk")
    .select("loan_status", count="exact")
    .limit(1)
    .execute()
)
print(
    "Supabase Data API: conexión correcta; "
    f"filas visibles con SELECT: {api_result.count or 0}"
)
