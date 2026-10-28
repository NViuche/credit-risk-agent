---
name: credit-risk
description: Calcula un Score de Riesgo de Impago (0-100), su categoría (BAJO / MODERADO / CRÍTICO) y la acción recomendada para una o varias operaciones de la tabla public.credit_risk de Supabase. Úsala siempre que haya que puntuar, priorizar o decidir acciones sobre préstamos de la cartera.
---

# Skill: Credit Risk & Default Calculator

## Qué hace
Convierte cuatro variables reales de cada préstamo de `public.credit_risk` en un **Score de Riesgo de Impago de 0 a 100** de forma determinista (misma entrada, misma salida), lo clasifica según la matriz de decisión de [AGENTS.md](../../AGENTS.md) y devuelve la acción sugerida.

## Cuándo usarla
- Después de consultar la cartera en Supabase con `execute_sql`, para puntuar cada préstamo devuelto.
- Para priorizar una lista de operaciones por riesgo o decidir la acción de cobro.
- **No** usarla para inventar datos: si falta una entrada obligatoria, se vuelve a consultar la base de datos.

## Entradas
| Campo | Columna en `credit_risk` | Tipo | Obligatorio |
| :--- | :--- | :--- | :--- |
| `loan_percent_income` | `loan_percent_income` | número (0 - 1) | Sí |
| `loan_int_rate` | `loan_int_rate` | número (%) o `null` | Sí (admite `null`) |
| `cb_person_default_on_file` | `cb_person_default_on_file` | `"Y"` / `"N"` | Sí |
| `loan_grade` | `loan_grade` | `"A"` … `"G"` | Sí |
| `id` | `id` | entero | Opcional (se devuelve tal cual) |

`loan_status` **no es una entrada**: es el resultado real (1 = impago). Solo se usa para validar el score.

## Fórmula
| Factor | Peso | Cálculo |
| :--- | :--- | :--- |
| Esfuerzo financiero | 35 | `min(loan_percent_income / 0.50, 1) × 35` |
| Tipo de interés | 25 | `clip((loan_int_rate − 5) / (23 − 5), 0, 1) × 25`; si es `null`, 12.5 y aviso |
| Impago previo en buró | 20 | `20` si `cb_person_default_on_file = 'Y'`, si no `0` |
| Grado del préstamo | 20 | A 0 · B 4 · C 8 · D 14 · E 17 · F 19 · G 20 |

## Salida
```json
{
  "id": 1,
  "score_riesgo": 76.17,
  "categoria": "CRÍTICO",
  "desglose_factores": {"esfuerzo_financiero": 28.0, "tipo_interes": 14.17, "impago_previo": 20.0, "grado_prestamo": 14.0},
  "accion_sugerida": "Generar orden de suspensión temporal de servicio y borrador de reclamo legal.",
  "requiere_autorizacion_humana": true,
  "avisos": []
}
```

| Score | Categoría | Acción | Autorización humana |
| :--- | :--- | :--- | :--- |
| < 30 | BAJO | Recordatorio amigable de pago | No |
| 30 - 65 | MODERADO | Congelar ampliación de crédito + plan en 3 cuotas | No |
| > 65 | CRÍTICO | Suspensión temporal + borrador de reclamación legal | **Sí** |

## Cómo invocarla
```powershell
'[{"id": 1, "loan_percent_income": 0.4, "loan_int_rate": 15.2, "cb_person_default_on_file": "Y", "loan_grade": "D"}]' | python skills/credit-risk/credit_risk.py
```
Acepta un objeto JSON o una lista. Desde Python: `from credit_risk import calculate_credit_risk`.

## Validación con datos reales
Aplicada a las 32.581 filas de `credit_risk` (detalle en [tests/pruebas.md](../../tests/pruebas.md)):

| Categoría | Préstamos | % cartera | Tasa de impago real |
| :--- | ---: | ---: | ---: |
| BAJO | 19.746 | 60,6 % | 8,2 % |
| MODERADO | 11.674 | 35,8 % | 39,8 % |
| CRÍTICO | 1.161 | 3,6 % | 72,1 % |

AUC del score frente a `loan_status`: **0,793**.

## Límites
- Pesos fijados por criterio experto y comprobados a posteriori; no es un modelo entrenado.
- El 9,6 % de las filas no tienen `loan_int_rate`; se imputa el punto medio y se informa en `avisos`.
- El dataset es crédito al consumo: aplicarlo a facturas B2B exige recalibrar.
