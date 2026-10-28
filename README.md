# Credit Risk & Default Intelligence

Proyecto de análisis de riesgo crediticio conectado a Supabase (PostgreSQL). La conexión anterior con MySQL de XAMPP no forma parte de este flujo.

## Preparación

1. Usa Python 3.12 o compatible.
2. Instala las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Configura `.env` con `SUPABASE_URL`, `SUPABASE_KEY` y `DATABASE_URL`. Usa `.env.example` como referencia. No compartas ni subas `.env` a Git.
4. Comprueba las conexiones:

   ```powershell
   python backend/test_conexion.py
   ```

El script prueba la tabla `credit_risk` mediante el SDK de Supabase y luego ejecuta una consulta PostgreSQL de solo lectura con `DATABASE_URL`. El SDK consulta la Data API; `DATABASE_URL` conecta directamente con PostgreSQL. Son dos vías de acceso distintas. La clave configurada debe tener permisos de lectura para la tabla; si la API devuelve un error de permisos, revisa que la tabla esté expuesta y sus políticas RLS permitan el `SELECT` correspondiente.

El resultado de la Data API informa cuántas filas son visibles para la clave y sus políticas. Un valor cero puede indicar una tabla vacía o que las políticas RLS no permiten ver filas.

Si aparece `Invalid API key`, sustituye `SUPABASE_KEY` por la clave **Publishable** del mismo proyecto Supabase (o una clave `anon` heredada válida). No uses la contraseña de PostgreSQL como API key ni publiques una clave `service_role`/secret.

## Estructura

```text
AGENTS.md                      Instrucciones del agente CreditGuard AI
REFLEXION.md                   Reflexión del equipo
.mcp.json                      MCP de Supabase (solo lectura)
skills/credit-risk/SKILL.md    Skill: qué hace, entradas, salida, validación
skills/credit-risk/credit_risk.py
tests/pruebas.md               Registro de pruebas
tests/test_credit_risk.py      Pruebas unitarias de la skill
backend/test_conexion.py       Prueba de conexión a Supabase
data/                          Fuente de datos y diccionario de credit_risk
investigacion/                 Problema, mercado, diagrama y diseño de la skill
```

## Pruebas de la skill

```powershell
python tests/test_credit_risk.py
```
