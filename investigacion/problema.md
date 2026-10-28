# Definición del Problema y Propuesta de Valor: CreditGuard AI

## 1. Problemas de BI evaluados
| # | Problema | Usuario | Datos reales disponibles | Decisión |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Riesgo de impago en una cartera de crédito** | Responsable de riesgos / cobros | Sí: Credit Risk Dataset (Kaggle, CC0) con el resultado real de impago | ✅ **Elegido** |
| 2 | Pérdida de clientes (churn) en SaaS B2B | Head of Customer Success | Solo datasets sintéticos o de telecomunicaciones | Descartado |
| 3 | Retraso en el cobro de facturas B2B (DSO) | CFO / tesorería | No encontramos datos públicos reales de facturas | Descartado (se usa como contexto de mercado) |
| 4 | Previsión de demanda en retail | Responsable de compras | Sí, pero el problema está muy cubierto por herramientas existentes | Descartado |
| 5 | Detección de fraude en pagos | Equipo antifraude | Datasets anonimizados (PCA) poco explicables | Descartado |

**Por qué el 1:** combina datos reales con resultado conocido (permite **validar** el sistema), una decisión de negocio clara (qué hacer con cada préstamo) y acciones sensibles donde tiene sentido exigir autorización humana.

## 2. Problema de Negocio
Los equipos de riesgo y cobros revisan la cartera de forma manual y reactiva: actúan cuando el impago ya se ha producido. Sin una priorización objetiva, el esfuerzo de cobro se reparte por igual entre préstamos de riesgo muy distinto, y las acciones duras (suspensión, reclamación legal) se deciden sin un criterio homogéneo.

## 3. Usuario Objetivo (Buyer Persona)
- **Rol principal:** analista o responsable de riesgo de crédito y cobros.
- **Decisor:** CFO / Director de Riesgos.
- **Necesidad:** saber en minutos qué préstamos de un segmento tienen más riesgo, cuánto importe está expuesto y qué acción tomar con cada uno, con una explicación que pueda defender.

## 4. Propuesta de Valor Agéntica
Un sistema agéntico que:
1. **Consulta** la cartera real en Supabase mediante MCP (solo lectura), en lenguaje natural.
2. **Puntúa** cada préstamo con una Skill propia determinista y explicable (Score 0-100 con desglose por factores).
3. **Prescribe** la acción según una matriz de severidad: recordatorio, plan de 3 cuotas o suspensión y reclamación legal.
4. **Respeta el control humano:** las acciones críticas quedan como propuestas pendientes de autorización.

## 5. Objetivos y KPI
| KPI | Definición | Valor medido |
| :--- | :--- | :--- |
| Tasa de impago de la cartera | `avg(loan_status)` | 21,82 % |
| Poder de discriminación del score | AUC del score frente a `loan_status` | 0,793 |
| Precisión de la alerta crítica | Tasa de impago real en la categoría CRÍTICO | 72,1 % (3,3 veces la media) |
| Importe en riesgo crítico | `sum(loan_amnt)` con score > 65 | 18.799.800 $ (6,0 % del total) |
| Tiempo de análisis | Desde la petición hasta el informe con acciones | Segundos (frente a revisión manual) |

**Objetivo de negocio:** concentrar el esfuerzo de cobro en el 3,6 % de préstamos CRÍTICOS y en el 35,8 % de MODERADOS, que juntos acumulan el 77 % de los impagos reales.
