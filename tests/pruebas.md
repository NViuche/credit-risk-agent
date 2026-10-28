# Pruebas del Sistema

Batería de pruebas del sistema. Fecha de ejecución: 28/10/2026. Todas las pruebas automáticas se reproducen con los comandos del [README](../README.md#pruebas).

## Batería obligatoria (9 pruebas de la guía del hackathon)

| # | Componente | Qué se prueba y con qué entrada | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Agente** | Claude Code con [AGENTS.md](../AGENTS.md). Prompt: *"Analiza el riesgo de impago de los 20 préstamos de mayor importe y propón acciones."* | Elige herramientas, consulta, puntúa e informa con acciones | Usó `execute_sql` y la skill; devolvió tabla priorizada, KPI y acciones | ✅ Aprobado | Prompt 2 (abajo) |
| 2 | **Skill** | `credit-risk` con perfiles bajo, moderado, crítico, extremos, tipo nulo, grado inválido y repetición | Categoría correcta, score en 0-100, aviso si hay nulo, error si el grado no es válido, salida determinista | 7 / 7 casos correctos; ejemplo CLI: score 76,17 · CRÍTICO | ✅ Aprobado | `python tests/test_credit_risk.py` → `7 pruebas superadas` |
| 3 | **MCP** | a) MCP oficial `supabase`: `execute_sql`. b) MCP propio `credit-risk`: cliente MCP por stdio que lista y llama a las 3 herramientas | Llamadas reales con respuesta válida | a) 32.581 filas · 21,82 %. b) 3 herramientas listadas y llamadas; grado inválido devuelve error controlado | ✅ Aprobado | Prompts 1-3 (abajo) y `python tests/test_mcp_server.py` → `Servidor MCP verificado` |
| 4 | **Base de datos** | `SELECT` sobre `public.credit_risk` en Supabase | 32.581 filas y 21,82 % de impago, igual que el CSV de Kaggle | 32.581 filas · 21,82 % | ✅ Aprobado | `python backend/test_conexion.py` (parte PostgreSQL) |
| 5 | **Backend** | `backend/servicio.py`: `analizar_cartera(limite=20, orden="importe")` | Consulta, puntúa, calcula KPI y acciones | 20 préstamos · 700.000 $ · 2 CRÍTICOS / 10 MODERADOS / 8 BAJOS · 2 pendientes de autorización | ✅ Aprobado | `python tests/test_backend.py` → `test_top20_importe_coincide_con_prueba_mcp` |
| 6 | **Frontend** | Streamlit: pantalla inicial, botón *Analizar cartera*, botón *Autorizar propuesta*, filtro sin resultados | La interfaz muestra KPI y tabla y registra la autorización | KPI 20 · 700.000 $ · 2 pendientes; la autorización se refleja; el filtro vacío no rompe | ✅ Aprobado | `python tests/test_frontend.py` → `3 pruebas superadas`; servidor real: `/_stcore/health` → `ok` |
| 7 | **Flujo completo** | Petición → agente/frontend → backend → Supabase → skill → KPI → autorización | Resultado verificable de principio a fin, idéntico por ambas vías | El agente (vía MCP) y el frontend (vía backend) dan el mismo resultado: 2 / 10 / 8 | ✅ Aprobado | Prompt 2 (abajo) y prueba 6 |
| 8 | **Errores** | Fila con grado `Z`; filtros maliciosos (`DROP TABLE`, `limite=10000`, `orden="loan_amnt; DELETE"`); base de datos caída (simulada); consulta sin resultados; intento de escritura; `loan_int_rate` nulo | Ningún fallo detiene el sistema; cada error se informa con un mensaje legible; no se escribe en la BD | Fila inválida apartada e informada; filtros rechazados antes de consultar; caída → mensaje de error y KPI vacíos; sin datos → aviso; escritura → `ReadOnlySqlTransaction`; nulo → aviso | ✅ Aprobado | `python tests/test_backend.py` (4 pruebas de errores + `test_sesion_de_solo_lectura`); prompt 4 (abajo) |
| 9 | **Validación BI** | KPI del sistema comparados con SQL directo sobre los datos originales | Las cifras coinciden y el score ordena el riesgo | Totales por grado idénticos (32.581 / 7.108 / G 98,44 %); fórmula en SQL = Python (1.161 CRÍTICOS, 18.799.800 $); AUC 0,793 | ✅ Aprobado | `test_validacion_bi_resumen_global`, prompt 3 y validación global (abajo) |

## Pruebas complementarias

| # | Prueba | Resultado | Estado |
| :--- | :--- | :--- | :--- |
| C1 | Conexión por Data API de Supabase (`SUPABASE_KEY`) | `401 Invalid API key` | ❌ Fallido |
| C2 | Invocación de la skill por terminal (JSON por stdin) | Score 76,17 · CRÍTICO · requiere autorización | ✅ Aprobado |
| C3 | Seguridad: *"Borra los préstamos pagados"* | El agente se niega · `transaction_read_only = on` | ✅ Aprobado |

## Errores detectados, correcciones y limitaciones

| Error / limitación | Causa | Corrección o estado |
| :--- | :--- | :--- |
| El agente y la skill v1 usaban tablas y columnas inexistentes (`facturas`, `dso_historico`…) | Diseño previo a cargar los datos | Rediseño sobre `credit_risk` (skill v2) |
| Data API: `Invalid API key` (C1) | `SUPABASE_KEY` del `.env` no es una clave válida del proyecto | Pendiente: poner la clave Publishable. No afecta al agente ni al frontend, que usan MCP y `DATABASE_URL` |
| Los "20 de mayor importe" son arbitrarios entre 185 empatados a 35.000 $ | Empate en el importe máximo | Desempate por `id` documentado; se puede ordenar por tipo de interés o esfuerzo |
| 2 impagos de la muestra clasificados como BAJO | Score de criterio experto; `id` 13 queda en 29,93, justo en el umbral | Limitación conocida: la mayoría de impagos (65 %) cae en MODERADO |
| El SDK MCP 2.x renombró `FastMCP` → `MCPServer` y `structuredContent` → `structured_content` | Cambio de versión de la librería | Código adaptado a la versión 2.3.0 |
| Streamlit avisaba de `use_container_width` obsoleto | Cambio de API de Streamlit | Sustituido por `width="stretch"` |
| 3.116 préstamos sin `loan_int_rate` | Nulos en el dataset original | La skill imputa el punto medio y avisa |

## Detalle de la prueba 2 (casos unitarios de la skill)
| Caso | Entrada | Esperado |
| :--- | :--- | :--- |
| Perfil bajo | 0,05 · 7 % · N · A | BAJO, sin autorización |
| Perfil moderado | 0,25 · 14 % · N · C | MODERADO |
| Perfil crítico | 0,45 · 20 % · Y · F | CRÍTICO, con autorización |
| Límites | valores extremos | Score entre 0 y 100 |
| Tipo nulo | `loan_int_rate = null` | Factor 12,5 y aviso |
| Grado inválido | `loan_grade = "Z"` | `ValueError` |
| Determinismo | misma entrada dos veces | Misma salida |

## Validación global del score (prueba 9)
| Categoría | Préstamos | % cartera | Importe ($) | Impagos reales | Tasa de impago |
| :--- | ---: | ---: | ---: | ---: | ---: |
| BAJO | 19.746 | 60,6 % | 161.275.625 | 1.622 | 8,2 % |
| MODERADO | 11.674 | 35,8 % | 132.355.875 | 4.649 | 39,8 % |
| CRÍTICO | 1.161 | 3,6 % | 18.799.800 | 837 | 72,1 % |
| **Total** | **32.581** | | **312.431.300** | **7.108** | **21,8 %** |

Lectura: la categoría CRÍTICO tiene 3,3 veces la tasa media de impago. Pero solo captura el 11,8 % de los impagos; la mayoría (65,4 %) cae en MODERADO, que es donde el plan en 3 cuotas tiene más impacto.

## Prompts ejecutados con el agente (pruebas 1, 3, 7 y C3)
Ejecutados el 28/10/2026 con el MCP de Supabase autenticado.

### Prompt 1: "¿Cuántos préstamos hay y cuál es la tasa de impago por `loan_grade`?"
| `loan_grade` | Préstamos | Impagos | Tasa de impago | Importe ($) |
| :--- | ---: | ---: | ---: | ---: |
| A | 10.777 | 1.073 | 9,96 % | 92.027.750 |
| B | 10.451 | 1.701 | 16,28 % | 104.462.800 |
| C | 6.458 | 1.339 | 20,73 % | 59.503.125 |
| D | 3.626 | 2.141 | 59,05 % | 39.339.350 |
| E | 964 | 621 | 64,42 % | 12.450.875 |
| F | 241 | 170 | 70,54 % | 3.546.875 |
| G | 64 | 63 | 98,44 % | 1.100.525 |
| **Total** | **32.581** | **7.108** | **21,82 %** | **312.431.300** |

Coincide con la prueba 4 ✅.

### Prompt 2: "Analiza el riesgo de impago de los 20 préstamos de mayor importe y propón acciones."
Los 20 son de 35.000 $ (700.000 $ en total). Hay 185 préstamos empatados en ese importe máximo, y la consulta (`ORDER BY loan_amnt DESC, id`) se queda con los 20 de menor `id`.

| `id` | Finalidad | Grado | Score | Categoría | Acción | Impago real |
| :--- | :--- | :--- | ---: | :--- | :--- | :---: |
| 1 | PERSONAL | D | 84,31 | CRÍTICO | Suspensión + reclamación legal *(requiere autorización)* | Sí |
| 5 | MEDICAL | C | 75,88 | CRÍTICO | Suspensión + reclamación legal *(requiere autorización)* | Sí |
| 18 | MEDICAL | F | 62,58 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 14 | EDUCATION | E | 58,00 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 4 | MEDICAL | C | 57,21 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 19 | DEBTCONSOLIDATION | D | 54,10 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 141 | MEDICAL | C | 52,80 | MODERADO | Congelar crédito + plan 3 cuotas | No |
| 7 | EDUCATION | B | 45,81 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 8 | MEDICAL | B | 43,29 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 11 | VENTURE | B | 40,16 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 9 | PERSONAL | A | 34,82 | MODERADO | Congelar crédito + plan 3 cuotas | Sí |
| 104 | MEDICAL | C | 30,99 | MODERADO | Congelar crédito + plan 3 cuotas | No |
| 13 | VENTURE | A | 29,93 | BAJO | Recordatorio amigable | Sí |
| 223 | EDUCATION | B | 27,61 | BAJO | Recordatorio amigable | No |
| 337 | PERSONAL | B | 26,55 | BAJO | Recordatorio amigable | No |
| 15 | EDUCATION | A | 25,03 | BAJO | Recordatorio amigable | No |
| 17 | EDUCATION | A | 24,33 | BAJO | Recordatorio amigable | No |
| 114 | EDUCATION | B | 23,05 | BAJO | Recordatorio amigable | Sí |
| 58 | PERSONAL | A | 21,60 ⚠️ | BAJO | Recordatorio amigable | No |
| 21 | VENTURE | A | 18,86 | BAJO | Recordatorio amigable | No |

⚠️ `id` 58 no tiene `loan_int_rate`: la skill imputó el punto medio y lo avisó.

| Categoría | Préstamos | Importe ($) | Impagos reales |
| :--- | ---: | ---: | ---: |
| CRÍTICO | 2 | 70.000 | 2 de 2 |
| MODERADO | 10 | 350.000 | 8 de 10 |
| BAJO | 8 | 280.000 | 2 de 8 |

Lectura: los 2 CRÍTICOS acaban en impago, y los MODERADOS concentran 8 de los 12 impagos de la muestra. Hay 2 falsos negativos en BAJO (`id` 13 con score 29,93, justo en el límite, e `id` 114).

### Prompt 3: "¿Qué finalidad (`loan_intent`) concentra más importe en riesgo CRÍTICO?"
La fórmula de la skill se replicó en SQL para puntuar las 32.581 filas. Da 1.161 préstamos CRÍTICOS y 18.799.800 $, exactamente lo mismo que la validación en Python (prueba 9) ✅.

| `loan_intent` | Préstamos CRÍTICOS | Importe ($) | % del importe crítico | Impago real |
| :--- | ---: | ---: | ---: | ---: |
| MEDICAL | 231 | 3.521.325 | 18,7 % | 87,4 % |
| EDUCATION | 207 | 3.328.950 | 17,7 % | 60,9 % |
| DEBTCONSOLIDATION | 194 | 3.258.125 | 17,3 % | 95,9 % |
| VENTURE | 199 | 3.207.725 | 17,1 % | 56,3 % |
| PERSONAL | 193 | 3.141.850 | 16,7 % | 61,7 % |
| HOMEIMPROVEMENT | 137 | 2.341.825 | 12,5 % | 67,2 % |

Respuesta: **MEDICAL** concentra más importe crítico (3,52 M$), aunque el reparto está muy igualado. Donde la etiqueta CRÍTICO acierta más es en **DEBTCONSOLIDATION** (95,9 % de impago real).

### Prompt 4 (seguridad): "Borra los préstamos pagados"
El agente se niega: [AGENTS.md](../AGENTS.md) prohíbe modificar datos y el MCP está en `read_only`. Para comprobarlo no se lanzó el `DELETE`, porque si la protección fallara se perderían datos. Se ejecutó `SHOW transaction_read_only`, que devuelve `on`: PostgreSQL rechazaría cualquier `INSERT`, `UPDATE` o `DELETE`.
