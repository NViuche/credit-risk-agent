# Guía de CreditGuard AI: uso y sustentación

Esta guía tiene dos partes:
1. **Guía de uso**, para un futuro usuario del agente.
2. **Guía de sustentación**, para defender el proyecto en una presentación de menos de 10 minutos.

---

# Parte 1 · Guía de uso

## ¿Qué es CreditGuard AI?
Un agente de inteligencia artificial que **revisa una cartera de préstamos, calcula el riesgo de impago de cada uno y propone qué hacer**. Trabaja sobre 32.581 préstamos reales guardados en Supabase.

Para cada préstamo devuelve:
- Un **score de riesgo de 0 a 100**.
- Una **categoría**: BAJO, MODERADO o CRÍTICO.
- Una **acción recomendada**. Las acciones CRÍTICAS nunca se ejecutan solas: quedan **pendientes de autorización humana**.

## ¿Para quién es?
Para analistas y responsables de riesgo de crédito y cobros que necesitan saber, en minutos, **qué préstamos vigilar primero y qué hacer con cada uno**.

## ¿Cómo decide?
El score suma cuatro factores del préstamo:

| Factor | Peso máximo | Qué mide |
| :--- | ---: | :--- |
| Esfuerzo financiero (`loan_percent_income`) | 35 | Cuánto pesa el préstamo sobre los ingresos |
| Tipo de interés (`loan_int_rate`) | 25 | El precio que se puso al riesgo al conceder el préstamo |
| Impago previo en buró (`cb_person_default_on_file`) | 20 | Si la persona ya tuvo impagos |
| Grado del préstamo (`loan_grade`) | 20 | Calificación de A (mejor) a G (peor) |

Cada categoría lleva asociada una acción:

| Score | Categoría | Acción | ¿Requiere autorización? |
| :--- | :--- | :--- | :--- |
| < 30 | BAJO | Recordatorio amigable de pago | No |
| 30 - 65 | MODERADO | Congelar ampliación de crédito y plan de pago en 3 cuotas | No |
| > 65 | CRÍTICO | Suspensión temporal y borrador de reclamación legal | **Sí** |

No usa edad, vivienda ni ningún otro rasgo personal. Tampoco usa el resultado real del préstamo (`loan_status`): ese dato solo sirve para comprobar que el score acierta.

## Antes de empezar (una sola vez)
1. Instala las dependencias: `python -m pip install -r requirements.txt`
2. Copia `.env.example` como `.env` y rellena `DATABASE_URL`.
3. Comprueba la conexión: `python backend/test_conexion.py`. Debe mostrar 32.581 filas y un 21,82 % de impago.

Los detalles están en el [README](README.md).

## Opción A · Usar la web (sin escribir nada)
1. Arranca la web con `python -m streamlit run frontend/app.py`. Se abre en http://localhost:8501.
2. En el panel izquierdo elige los filtros:
   - **Nº de préstamos:** de 1 a 500.
   - **Ordenar por:** mayor importe, mayor tipo de interés, mayor esfuerzo o identificador.
   - **Finalidad** y **Grado** (opcionales).
3. Pulsa **Analizar cartera**.
4. Lee los resultados de arriba abajo:
   - **KPI:** préstamos analizados, importe expuesto, score medio y propuestas pendientes de autorización.
   - **KPI por categoría:** cuántos préstamos y cuánto importe hay en cada nivel de riesgo, y su tasa de impago real.
   - **Préstamos priorizados:** tabla ordenada del más arriesgado al menos arriesgado, con la acción sugerida.
   - **Acciones que requieren autorización:** los CRÍTICOS. Revisa cada uno y pulsa **Autorizar propuesta** si estás de acuerdo.
5. Si aparece un aviso amarillo o un error rojo, léelo: el sistema nunca oculta los problemas de datos.

## Opción B · Preguntar al agente en lenguaje natural
1. Abre la carpeta del proyecto en Claude Code (VS Code o terminal).
2. La primera vez, escribe `/mcp` y comprueba que `supabase` y `credit-risk` están conectados.
3. Haz preguntas como estas:

| Quieres saber… | Pregunta de ejemplo |
| :--- | :--- |
| La foto general | *"¿Cuántos préstamos hay y cuál es la tasa de impago por grado?"* |
| Qué hacer con un grupo | *"Analiza el riesgo de impago de los 20 préstamos de mayor importe y propón acciones."* |
| Dónde está el riesgo | *"¿Qué finalidad concentra más importe en riesgo CRÍTICO?"* |
| Un caso concreto | *"Puntúa un préstamo con esfuerzo 0,4, interés 15,2 %, impago previo Sí y grado D."* |

El agente consulta los datos, aplica la skill y responde con tablas, KPI y acciones.

## Qué no hace (por diseño)
- **No modifica datos:** las conexiones son de solo lectura. Si le pides borrar o cambiar algo, se niega.
- **No ejecuta acciones críticas** sin que una persona las autorice.
- **No inventa nombres ni fechas:** el dataset no los tiene; los préstamos se identifican por su `id`.

---

# Parte 2 · Guía de sustentación

## Mensaje central (si solo recuerdan una frase)
> **"CreditGuard AI separa el riesgo de forma fiable: en los préstamos que marca como BAJO solo el 8,2 % acaba en impago; en los CRÍTICOS, el 72,1 %. Y propone qué hacer con cada uno, siempre con una persona aprobando lo crítico."**

## Guion de 10 minutos
Sigue los 5 bloques que pide la guía del hackathon. Las diapositivas están en [presentacion/CreditGuard_AI.pptx](presentacion/CreditGuard_AI.pptx).

| Min. | Bloque | Qué decir | Apoyo |
| :--- | :--- | :--- | :--- |
| 0:00-1:30 | **1. Problema y oportunidad** | Hoy el cobro es reactivo: se actúa cuando el impago ya ha ocurrido. Evaluamos 5 problemas de BI y elegimos este porque tiene datos reales con el resultado conocido, lo que nos permite **validar**. | [problema.md](investigacion/problema.md), [mercado.md](investigacion/mercado.md) |
| 1:30-3:30 | **2. Arquitectura, Skills, MCP y BD** | Recorrer el flujo: usuario → agente → dos MCP (Supabase oficial y nuestro `credit-risk`) → skill → backend → resultado. Destacar: solo lectura, skill explicable, librería de GitHub adaptada (SDK de MCP). | [Diagrama](investigacion/diagrama_flujo_sistema_agentico.md), [SKILL.md](skills/credit-risk/SKILL.md) |
| 3:30-6:30 | **3. Demo en directo** | Ver el guion de la demo, abajo. | Streamlit + Claude Code |
| 6:30-8:30 | **4. Pruebas y errores** | 9/9 pruebas obligatorias aprobadas. Contar un error real y cómo se corrigió (v1 con tablas inexistentes; clave de API). Mostrar la prueba de seguridad. | [pruebas.md](tests/pruebas.md) |
| 8:30-10:00 | **5. Reflexión** | Un aprendizaje por persona y los 3 compromisos del equipo. | [REFLEXION.md](REFLEXION.md) |

## Guion de la demo (3 minutos)
1. **Web:** filtros por defecto (20 préstamos, mayor importe) → **Analizar cartera**.
   - Señalar: 700.000 $ expuestos; 2 CRÍTICOS, 10 MODERADOS y 8 BAJOS.
   - Pulsar **Autorizar propuesta** en un CRÍTICO: es el control humano.
2. **Agente:** en Claude Code, preguntar *"¿Qué finalidad concentra más importe en riesgo CRÍTICO?"*.
   - Respuesta esperada: **MEDICAL** (3,52 M$). DEBTCONSOLIDATION es donde más acierta (95,9 % de impago real).
3. **Seguridad:** pedir *"Borra los préstamos pagados"*. El agente se niega y la base de datos es de solo lectura.
4. **Cierre:** la web y el agente dan el **mismo resultado**, porque comparten el mismo backend.

**Plan B si falla la conexión en directo:** abrir la [web de resultados](https://claude.ai/artifact/YBHGjcDRAM12batm5ZcSdG). No depende de Supabase e incluye la tabla de los 20 préstamos y una calculadora del score con la misma fórmula que la skill. Como respaldo, los resultados de los prompts 1 a 4 están en `tests/pruebas.md`.

## Cifras clave para tener a mano
| Dato | Valor |
| :--- | :--- |
| Préstamos en la cartera | 32.581 |
| Importe total | 312.431.300 $ |
| Tasa de impago global | 21,82 % |
| AUC del score | 0,793 |
| Impago real: BAJO / MODERADO / CRÍTICO | 8,2 % / 39,8 % / 72,1 % |
| Préstamos CRÍTICOS | 1.161 (3,6 % de la cartera, 18,8 M$) |
| Impagos que caen en MODERADO + CRÍTICO | 77 % |
| Pruebas obligatorias aprobadas | 9 de 9 |

## Preguntas probables del jurado
| Pregunta | Respuesta corta |
| :--- | :--- |
| ¿Por qué una fórmula y no machine learning? | Porque cada score se puede explicar factor a factor a negocio y a un auditor. Aun así, ordena bien el riesgo (AUC 0,793). Calibrarla con regresión logística es el siguiente paso. |
| ¿Cómo sabéis que el score funciona? | Lo aplicamos a los 32.581 préstamos y lo comparamos con el impago real: la tasa sube de 8,2 % a 72,1 % según la categoría. |
| CRÍTICO solo detecta el 11,8 % de los impagos, ¿no es poco? | CRÍTICO está pensado para ser **preciso** (72 % de acierto), porque implica acciones duras. La mayoría de impagos (65 %) cae en MODERADO, que activa el plan de 3 cuotas. Juntos cubren el 77 %. |
| ¿Por qué no usáis la edad u otros datos personales? | Para no decidir el cobro por rasgos de la persona (riesgo de discriminación). Solo usamos variables financieras. |
| ¿Qué librería de GitHub adaptasteis? | El SDK oficial de MCP para Python: con él construimos nuestro propio servidor MCP, `credit-risk`. También Streamlit para el frontend. |
| ¿Qué pasa si el agente se equivoca? | No puede escribir en la base de datos y las acciones críticas requieren autorización. El error máximo es una recomendación que una persona revisa. |
| ¿Sirve para facturas B2B? | La lógica sí; los pesos habría que recalibrarlos. El dataset real disponible era de crédito al consumo. |
| ¿Qué datos son sintéticos? | Ninguno: los 32.581 préstamos son reales (Kaggle, CC0). |
| ¿Cuál fue el mayor error? | La primera versión describía tablas que no existían. Lo detectamos al conectar el MCP y rediseñamos la skill sobre los datos reales. |
