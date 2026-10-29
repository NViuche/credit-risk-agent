# Guía de CreditGuard AI

CreditGuard AI es un agente de inteligencia artificial que **revisa una cartera de préstamos, calcula el riesgo de impago de cada uno y propone qué hacer**. Esta guía explica qué problema resuelve, cómo funciona, cómo usarlo y qué límites tiene.

Material relacionado: [diapositivas](presentacion/CreditGuard_AI.pptx) · [web de resultados](https://claude.ai/artifact/YBHGjcDRAM12batm5ZcSdG).

---

## 1. El problema que resuelve
En muchas empresas, el cobro es **reactivo**: se actúa cuando el impago ya ha ocurrido. La cartera se revisa a mano y el esfuerzo se reparte igual entre préstamos de riesgo muy distinto.

Las herramientas habituales no resuelven esto del todo:

| Herramienta | Qué hace | Qué le falta |
| :--- | :--- | :--- |
| ERP y contabilidad (SAP, NetSuite…) | Informes estáticos de deuda | Revisión 100 % manual |
| Automatización de cobros (Chaser, HighRadius…) | Envía avisos según reglas simples | No anticipa el riesgo |
| Scoring externo (Experian, D&B…) | Da una puntuación de crédito | No dice qué acción tomar |

CreditGuard AI cubre ese hueco: **consulta los datos, puntúa el riesgo de forma explicable y propone la acción**, con una persona aprobando las decisiones importantes.

Antes de elegir este problema se valoraron otros cuatro: pérdida de clientes en SaaS, retraso de cobro de facturas B2B, previsión de demanda y fraude en pagos. Se eligió el riesgo de impago porque existen datos reales con el resultado conocido, lo que permite comprobar si el sistema acierta. Detalle en [investigacion/problema.md](investigacion/problema.md) y [investigacion/mercado.md](investigacion/mercado.md).

## 2. Los datos
| Dato | Valor |
| :--- | :--- |
| Préstamos | 32.581, reales (Credit Risk Dataset de Kaggle, licencia CC0) |
| Importe total | 312.431.300 $ |
| Tasa de impago global | 21,82 % |
| Dónde están | Supabase (PostgreSQL), tabla `public.credit_risk` |

- **Sin datos personales:** no hay nombres, documentos ni fechas. Cada préstamo se identifica por su `id`.
- **Calidad revisada:** el 9,6 % de los préstamos no tiene tipo de interés, hay 7 edades imposibles y 165 filas duplicadas. Todo está documentado en [data/diccionario_de_datos.md](data/diccionario_de_datos.md).

## 3. Cómo está construido
```text
Usuario ──► Agente CreditGuard ──► MCP de Supabase (consultas SQL, solo lectura) ──► Base de datos
            (Claude Code)    └──► MCP propio credit-risk ──► Backend + Skill ──► Resultado BI
Web Streamlit ─────────────────────────────────────────────► Backend + Skill ──► Resultado BI
```

| Pieza | Para qué sirve |
| :--- | :--- |
| **Agente** ([AGENTS.md](AGENTS.md)) | Entiende la pregunta, elige la herramienta y redacta el informe |
| **MCP de Supabase** | Permite al agente consultar la base de datos con SQL, solo en lectura |
| **MCP propio `credit-risk`** | Servidor propio, hecho adaptando el SDK oficial de MCP (librería de GitHub), con 3 herramientas: analizar una cartera, puntuar un préstamo y resumir la cartera |
| **Skill `credit-risk`** | La fórmula que calcula el score de riesgo |
| **Backend** | Une datos, skill y KPI. Tanto la web como el agente lo usan, por eso dan el mismo resultado |
| **Web (Streamlit)** | Interfaz para usar el sistema sin escribir preguntas |

## 4. Cómo decide: la Skill
El **score de riesgo va de 0 a 100** y suma cuatro factores del préstamo:

| Factor | Peso máximo | Qué mide |
| :--- | ---: | :--- |
| Esfuerzo financiero (`loan_percent_income`) | 35 | Cuánto pesa el préstamo sobre los ingresos |
| Tipo de interés (`loan_int_rate`) | 25 | El precio que se puso al riesgo al conceder el préstamo |
| Impago previo en buró (`cb_person_default_on_file`) | 20 | Si la persona ya tuvo impagos |
| Grado del préstamo (`loan_grade`) | 20 | Calificación de A (mejor) a G (peor) |

Según el score, el agente propone una acción:

| Score | Categoría | Acción | ¿Requiere autorización? |
| :--- | :--- | :--- | :--- |
| < 30 | BAJO | Recordatorio amigable de pago | No |
| 30 - 65 | MODERADO | Congelar ampliación de crédito y plan de pago en 3 cuotas | No |
| > 65 | CRÍTICO | Suspensión temporal y borrador de reclamación legal | **Sí** |

**Ejemplo:** esfuerzo 0,4, interés 15,2 %, impago previo Sí y grado D dan un score de **76,17**: CRÍTICO.

- **Qué no usa:** edad, vivienda ni otros rasgos personales, para no decidir el cobro por características de la persona.
- **Qué usa solo para comprobar:** el resultado real del préstamo (`loan_status`). Nunca entra en el cálculo.

El detalle de la fórmula está en [skills/credit-risk/SKILL.md](skills/credit-risk/SKILL.md).

## 5. ¿Acierta? Resultados con datos reales
La skill se aplicó a los 32.581 préstamos y se comparó con lo que pasó de verdad:

| Categoría | Préstamos | % de la cartera | Importe | Impago real |
| :--- | ---: | ---: | ---: | ---: |
| BAJO | 19.746 | 60,6 % | 161.275.625 $ | 8,2 % |
| MODERADO | 11.674 | 35,8 % | 132.355.875 $ | 39,8 % |
| CRÍTICO | 1.161 | 3,6 % | 18.799.800 $ | 72,1 % |

- **Cuanto más alta la categoría, más impagos reales.** En CRÍTICO, la tasa de impago es 3,3 veces la media.
- **AUC de 0,793:** el score ordena bien el riesgo (0,5 sería azar).
- **El 77 % de los impagos** cae en MODERADO o CRÍTICO, las dos categorías con acción de cobro.

## 6. Cómo usarlo

### Antes de empezar (una sola vez)
Los comandos de esta guía se ejecutan en la terminal de VS Code:
1. Abre la carpeta del proyecto en VS Code: **File → Open Folder** y elige la carpeta que contiene `requirements.txt`.
2. Abre la terminal: **Terminal → New Terminal** (atajo `` Ctrl+` ``, o `Ctrl+ñ` en teclado español). Se abre ya situada en la carpeta del proyecto.
3. Instala las dependencias. Pega este comando en la terminal y pulsa Enter:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Copia `.env.example` como `.env` (desde el explorador de VS Code o con `copy .env.example .env` en la terminal), ábrelo y rellena `DATABASE_URL`.
5. Comprueba la conexión desde la terminal con `python backend/test_conexion.py`. Debe mostrar 32.581 filas y un 21,82 % de impago.

### Opción A · La web
1. Arranca la web desde la terminal de VS Code con `python -m streamlit run frontend/app.py`. Se abre en el navegador en http://localhost:8501, una dirección de tu propio ordenador que funciona mientras la terminal siga abierta.
2. Elige los filtros en el panel izquierdo:
   - **Nº de préstamos:** de 1 a 500.
   - **Ordenar por:** mayor importe, mayor tipo de interés, mayor esfuerzo o identificador.
   - **Finalidad** y **Grado** (opcionales).
3. Pulsa **Analizar cartera**.
4. Revisa los resultados:
   - **KPI:** préstamos analizados, importe expuesto, score medio y propuestas pendientes de autorización.
   - **KPI por categoría:** préstamos, importe y tasa de impago real en cada nivel de riesgo.
   - **Préstamos priorizados:** del más arriesgado al menos arriesgado, con su acción.
   - **Acciones que requieren autorización:** los CRÍTICOS. Pulsa **Autorizar propuesta** en cada uno con el que estés de acuerdo.
5. Si aparece un aviso amarillo o un error rojo, léelo: el sistema nunca oculta los problemas de datos.

### Opción B · Preguntar al agente
1. Abre la carpeta del proyecto en Claude Code (VS Code o terminal).
2. La primera vez, escribe `/mcp` y comprueba que `supabase` y `credit-risk` están conectados.
3. Pregunta en lenguaje natural:

| Quieres saber… | Pregunta de ejemplo |
| :--- | :--- |
| La foto general | *"¿Cuántos préstamos hay y cuál es la tasa de impago por grado?"* |
| Qué hacer con un grupo | *"Analiza el riesgo de impago de los 20 préstamos de mayor importe y propón acciones."* |
| Dónde está el riesgo | *"¿Qué finalidad concentra más importe en riesgo CRÍTICO?"* |
| Un caso concreto | *"Puntúa un préstamo con esfuerzo 0,4, interés 15,2 %, impago previo Sí y grado D."* |

### Ejemplo de resultado
Con la pregunta de los **20 préstamos de mayor importe** (700.000 $ en total), el resultado es este:

| Categoría | Préstamos | Importe | Impagos reales |
| :--- | ---: | ---: | ---: |
| CRÍTICO | 2 | 70.000 $ | 2 de 2 |
| MODERADO | 10 | 350.000 $ | 8 de 10 |
| BAJO | 8 | 280.000 $ | 2 de 8 |

Los 2 CRÍTICOS (`id` 1 y 5) quedan como **propuestas pendientes de autorización**. La web y el agente dan el mismo resultado.

Por finalidad, **Médica** concentra más importe en riesgo crítico (3,52 M$). En **Consolidación de deuda** la etiqueta CRÍTICO acierta más: el 95,9 % de esos préstamos impagó.

## 7. Garantías: pruebas y seguridad
- **9 de 9 pruebas obligatorias aprobadas:** agente, skill, MCP, base de datos, backend, web, flujo completo, gestión de errores y validación de las cifras. Cada una tiene su evidencia en [tests/pruebas.md](tests/pruebas.md).
- **22 pruebas automáticas.** Se pueden repetir con los comandos del [README](README.md#pruebas).
- **No modifica datos:** las conexiones son de solo lectura. Si se le pide borrar o cambiar algo, el agente se niega y la base de datos lo rechazaría igualmente.
- **No ejecuta acciones críticas** sin que una persona las autorice.
- **No inventa nombres ni fechas:** el dataset no los tiene.
- **Errores encontrados y corregidos:**
  - La primera versión usaba tablas que no existían; se rediseñó sobre los datos reales.
  - La clave de la API de Supabase no era válida; se corrigió.
  - La versión 2.x del SDK de MCP cambió nombres; el código se adaptó.

## 8. Límites
| Límite | Qué implica |
| :--- | :--- |
| Crédito al consumo, no B2B | La lógica sirve para facturas, pero los pesos habría que recalibrarlos |
| Pesos de criterio experto | Ordenan bien el riesgo, pero no están entrenados con un modelo estadístico |
| CRÍTICO es preciso, no exhaustivo | Captura el 11,8 % de los impagos; la mayoría (65 %) cae en MODERADO |
| Datos sin fechas | No se puede medir el DSO ni la evolución en el tiempo |
| Tipos de interés incompletos | En el 9,6 % de los préstamos se imputa el punto medio, y se avisa |

**Siguiente mejora prevista:** calibrar los pesos con regresión logística y compararla con la fórmula actual.

## 9. Lo aprendido
- **Datos primero:** el sistema se diseña sobre lo que hay realmente en la base de datos.
- **La IA se revisa:** sus resultados se contrastan con consultas directas a los datos.
- **Persona al mando:** las decisiones duras de cobro siempre las autoriza alguien.

La reflexión completa del equipo está en [REFLEXION.md](REFLEXION.md).

## Preguntas frecuentes
| Pregunta | Respuesta |
| :--- | :--- |
| ¿Por qué una fórmula y no un modelo de machine learning? | Porque cada score se explica factor a factor. Aun así, ordena bien el riesgo (AUC 0,793). |
| ¿Por qué CRÍTICO detecta tan pocos impagos? | Porque implica acciones duras y está pensado para equivocarse poco (72 % de acierto). Los demás impagos de riesgo caen en MODERADO, que activa el plan de 3 cuotas. |
| ¿Hay datos inventados? | No. Los 32.581 préstamos son reales. |
| ¿Qué pasa si el agente se equivoca? | No puede escribir en la base de datos y lo crítico requiere autorización, así que un error se queda en una recomendación que revisa una persona. |
| ¿Sirve para facturas entre empresas? | La lógica sí; los pesos habría que ajustarlos a esos datos. |
