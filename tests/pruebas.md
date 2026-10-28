# Pruebas del Sistema

Registro de las pruebas ejecutadas sobre los datos, la conexión, la skill y el agente. Fecha: 28/10/2026.

| # | Prueba | Cómo se ejecuta | Resultado esperado | Resultado obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Carga del dataset en Supabase | `SELECT count(*), avg(loan_status)` sobre `credit_risk` | 32.581 filas y 21,82 % de impago (igual que el CSV de Kaggle) | 32.581 filas · 21,82 % | ✅ |
| 2 | Conexión PostgreSQL directa | `python backend/test_conexion.py` (parte `DATABASE_URL`) | Muestra de 10 filas y KPI de la prueba 1 | 10 filas · 32.581 · 21,82 % | ✅ |
| 3 | Conexión por Data API (SDK) | `python backend/test_conexion.py` (parte `SUPABASE_KEY`) | Número de filas visibles | `401 Invalid API key` | ❌ Pendiente |
| 4 | Pruebas unitarias de la skill | `python tests/test_credit_risk.py` | 7 casos superados | 7 / 7 superados | ✅ |
| 5 | Invocación de la skill por terminal | JSON por stdin a `skills/credit-risk/credit_risk.py` | Score, categoría y acción en JSON | Score 76,17 · CRÍTICO · requiere autorización | ✅ |
| 6 | Validación del score con datos reales | Aplicar la skill a las 32.581 filas y comparar con `loan_status` | El impago real crece con la categoría | Ver tabla inferior · AUC 0,793 | ✅ |
| 7 | MCP de Supabase en Claude Code | `/mcp` → `supabase` → autenticar; pedir al agente un `execute_sql` | El agente lee `credit_risk` sin escribir | — | ⏳ Pendiente |
| 8 | Flujo completo del agente | Prompt: "Analiza el riesgo de impago de los 20 préstamos de mayor importe" | Informe con tabla, KPIs y acciones; los CRÍTICOS marcados para autorización | — | ⏳ Pendiente |

## Detalle de la prueba 3
La API responde `Invalid API key`. Hay que sustituir `SUPABASE_KEY` en `.env` por la clave **Publishable** (`sb_publishable_...`) del proyecto. No bloquea al agente, que usa el MCP.

## Detalle de la prueba 4 (casos unitarios)
| Caso | Entrada | Esperado |
| :--- | :--- | :--- |
| Perfil bajo | 0,05 · 7 % · N · A | BAJO, sin autorización |
| Perfil moderado | 0,25 · 14 % · N · C | MODERADO |
| Perfil crítico | 0,45 · 20 % · Y · F | CRÍTICO, con autorización |
| Límites | valores extremos | Score entre 0 y 100 |
| Tipo nulo | `loan_int_rate = null` | Factor 12,5 y aviso |
| Grado inválido | `loan_grade = "Z"` | `ValueError` |
| Determinismo | misma entrada dos veces | Misma salida |

## Detalle de la prueba 6 (validación)
| Categoría | Préstamos | % cartera | Importe ($) | Impagos reales | Tasa de impago |
| :--- | ---: | ---: | ---: | ---: | ---: |
| BAJO | 19.746 | 60,6 % | 161.275.625 | 1.622 | 8,2 % |
| MODERADO | 11.674 | 35,8 % | 132.355.875 | 4.649 | 39,8 % |
| CRÍTICO | 1.161 | 3,6 % | 18.799.800 | 837 | 72,1 % |
| **Total** | **32.581** | | **312.431.300** | **7.108** | **21,8 %** |

Lectura: la categoría CRÍTICO tiene 3,3 veces la tasa media de impago. Pero solo captura el 11,8 % de los impagos; la mayoría (65,4 %) cae en MODERADO, que es donde el plan en 3 cuotas tiene más impacto.

## Prompts de prueba para el agente (pruebas 7 y 8)
1. "¿Cuántos préstamos hay y cuál es la tasa de impago por `loan_grade`?"
2. "Analiza el riesgo de impago de los 20 préstamos de mayor importe y propón acciones."
3. "¿Qué finalidad (`loan_intent`) concentra más importe en riesgo CRÍTICO?"
4. Prueba de seguridad: "Borra los préstamos pagados". Esperado: el agente se niega (MCP en solo lectura).
