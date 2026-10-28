# Diseño de la Skill: Credit Risk & Default Probability Calculator

El contrato operativo (entradas, salida, cómo invocarla) está en [skills/credit-risk/SKILL.md](../skills/credit-risk/SKILL.md). Este documento explica **por qué** está diseñada así.

## Evolución
- **v1 (descartada):** usaba `dso_historico`, `porcentaje_credito_usado`, `dias_vencido` e `incidentes_pago_6m`. Ninguna de esas columnas existe en Supabase, así que el agente no podía alimentarla con datos reales.
- **v2 (actual):** usa solo columnas reales de `public.credit_risk`, para que el 100 % del cálculo salga de datos consultados y no inventados.

## Elección de variables
| Variable | Por qué |
| :--- | :--- |
| `loan_percent_income` | Mide el esfuerzo de pago: cuanto más pesa la cuota sobre los ingresos, más probable el impago. Mayor peso (35). |
| `loan_int_rate` | Es el precio que el prestamista ya asignó al riesgo. Peso 25. |
| `cb_person_default_on_file` | Un impago previo es el mejor predictor conductual disponible. Peso 20. |
| `loan_grade` | Calificación interna; el impago salta del 20,7 % (C) al 59,1 % (D), por eso los puntos crecen más a partir de D. Peso 20. |

Se excluyen a propósito:
- `loan_status`, porque es el resultado que queremos predecir (sería hacer trampa).
- Edad, vivienda y finalidad, para no tomar decisiones de cobro basadas en rasgos personales.

## Reglas de Cálculo (Fórmula)
1. **Esfuerzo financiero (35):** `min(loan_percent_income / 0.50, 1) × 35`
2. **Tipo de interés (25):** `clip((loan_int_rate − 5) / 18, 0, 1) × 25`; nulo → 12,5
3. **Impago previo (20):** `Y` → 20, `N` → 0
4. **Grado (20):** A 0 · B 4 · C 8 · D 14 · E 17 · F 19 · G 20

**Puntuación Total de Riesgo:** suma de los 4 factores (0 = riesgo nulo, 100 = impago casi seguro).

## Matriz de Decisiones para el Agente
- **Score < 30 (Riesgo Bajo):** recordatorio cordial de pago.
- **Score 30 - 65 (Riesgo Moderado):** bloquear ampliación de crédito y sugerir plan de pago a 3 plazos.
- **Score > 65 (Riesgo Alto / Crítico):** proponer suspensión temporal y derivar a jurídico o recobro intensivo, **con autorización humana**.

## Resultado de la validación
Sobre las 32.581 filas: la tasa de impago real es 8,2 % en BAJO, 39,8 % en MODERADO y 72,1 % en CRÍTICO, con un AUC de 0,793. La escala ordena bien el riesgo. Ver [tests/pruebas.md](../tests/pruebas.md).
