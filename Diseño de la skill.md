# Skill: Credit Risk & Default Probability Calculator

## Descripción
Evalúa los datos de facturación e historial financiero de un cliente para calcular el Score de Riesgo de Impago (0 a 100) y clasificar la severidad.

## Entrada (Input JSON)
- `dso_historico` (integer)
- `porcentaje_credito_usado` (float)
- `dias_vencido_factura_actual` (integer)
- `incidentes_pago_6m` (integer)

## Reglas de Cálculo (Fórmula)
1. **Factor Vencimiento Actual (40% peso):** `min(dias_vencido_factura_actual * 2, 40)`
2. **Factor Uso de Crédito (20% peso):** `si porcentaje_credito_usado > 80% -> 20 pto, sino -> 5 pto`
3. **Factor Incidentes Previos (20% peso):** `incidentes_pago_6m * 10` (máximo 20)
4. **Factor DSO (20% peso):** `si dso_historico > 45 dias -> 20 pto, sino -> 5 pto`

**Puntuación Total de Riesgo:** Suma de los 4 factores (0 = Riesgo Nulo, 100 = Impago Casi Seguro).

## Matriz de Decisiones para el Agente
- **Score < 30 (Riesgo Bajo):** Generar recordatorio cordial de pago 5 días antes del vencimiento.
- **Score 30 - 65 (Riesgo Moderado):** Bloquear ampliación de crédito y sugerir plan de pago a 3 plazos.
- **Score > 65 (Riesgo Alto / Crítico):** Recomendar suspensión inmediata de servicio/licencia y derivar a departamento jurídico o recobro intensivo.