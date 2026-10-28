# Documentación del Dataset y Calidad de Datos

## 1. Fuente y Origen de los Datos
* **Nombre del Dataset Original:** Credit Risk Dataset.
* **Fuente:** Kaggle (público / open data).
* **Entorno de Despliegue:** Supabase (PostgreSQL gestionado), proyecto `ocigjzqtakriuajyfnbx`.
* **Contexto de Dominio:** Cartera de préstamos con su resultado real (impago o no), usada para evaluar la morosidad y la capacidad crediticia.

---

## 2. Licencia y Términos de Uso
* **Tipo de Licencia:** CC0: Public Domain / Open Data License.
* **Uso Permitido:** Libre para investigación, desarrollo académico, prototipado y evaluaciones tecnológicas (Hackathons).
* **Privacidad y GDPR/LOPD:** El conjunto de datos no contiene datos personales identificables (PII): no hay nombres, documentos ni fechas. Cada fila se identifica con un `id` numérico secuencial añadido en la carga.

---

## 3. Estructura de la Base de Datos

Una única tabla: **`public.credit_risk`**, con **32.581 filas** (una por préstamo) y **13 columnas**. Tasa de impago global (`loan_status = 1`): **21,82 %**.

El detalle de columnas, tipos y calidad está en [diccionario_de_datos.md](diccionario_de_datos.md).

### Acceso
| Vía | Uso | Configuración |
| :--- | :--- | :--- |
| MCP de Supabase (`execute_sql`) | El agente consulta la tabla desde Claude Code | [.mcp.json](../.mcp.json), modo `read_only` |
| PostgreSQL directo (`DATABASE_URL`) | Scripts Python y pruebas | `.env` (no versionado) |
| Data API (`SUPABASE_URL` + `SUPABASE_KEY`) | SDK de Supabase | `.env`; RLS activado en la tabla |
