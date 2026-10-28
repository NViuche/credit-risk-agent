# Diccionario de Datos

## Tabla: `public.credit_risk`

32.581 filas · 13 columnas · RLS activado.

| Columna | Tipo | Descripción | Valores / rango | Nulos | Uso en el agente |
| :--- | :--- | :--- | :--- | ---: | :--- |
| `id` | `bigint` | Identificador del préstamo (añadido en la carga) | 1 - 32.581 | 0 | Clave |
| `person_age` | `integer` | Edad del prestatario | 20 - 144 (mediana 26) | 0 | Contexto |
| `person_income` | `integer` | Ingresos anuales ($) | 4.000 - 6.000.000 (mediana 55.000) | 0 | Contexto |
| `person_home_ownership` | `text` | Régimen de vivienda | `RENT`, `MORTGAGE`, `OWN`, `OTHER` | 0 | Segmentación |
| `person_emp_length` | `numeric` | Años de antigüedad laboral | 0 - 123 (mediana 4) | 895 | Contexto |
| `loan_intent` | `text` | Finalidad del préstamo | `EDUCATION`, `MEDICAL`, `VENTURE`, `PERSONAL`, `DEBTCONSOLIDATION`, `HOMEIMPROVEMENT` | 0 | Segmentación |
| `loan_grade` | `text` | Grado de calidad del préstamo | `A` (mejor) … `G` (peor) | 0 | **Entrada skill** |
| `loan_amnt` | `integer` | Importe del préstamo ($) | 500 - 35.000 (mediana 8.000) | 0 | Importe expuesto |
| `loan_int_rate` | `numeric` | Tipo de interés (%) | 5,42 - 23,22 | 3.116 | **Entrada skill** |
| `loan_status` | `smallint` | Resultado real: 1 = impago, 0 = al corriente | 0 / 1 (21,82 % impago) | 0 | Validación (nunca entrada) |
| `loan_percent_income` | `numeric` | Importe del préstamo / ingresos anuales | 0,00 - 0,83 | 0 | **Entrada skill** |
| `cb_person_default_on_file` | `text` | Impago previo registrado en buró | `Y` (5.745) / `N` (26.836) | 0 | **Entrada skill** |
| `cb_person_cred_hist_length` | `integer` | Años de historial crediticio | 2 - 30 (mediana 4) | 0 | Contexto |

### Tasa de impago por segmento (dato real)

| `loan_grade` | Préstamos | Impago | | `loan_intent` | Préstamos | Impago |
| :--- | ---: | ---: | --- | :--- | ---: | ---: |
| A | 10.777 | 9,96 % | | DEBTCONSOLIDATION | 5.212 | 28,6 % |
| B | 10.451 | 16,28 % | | MEDICAL | 6.071 | 26,7 % |
| C | 6.458 | 20,73 % | | HOMEIMPROVEMENT | 3.605 | 26,1 % |
| D | 3.626 | 59,05 % | | PERSONAL | 5.521 | 19,9 % |
| E | 964 | 64,42 % | | EDUCATION | 6.453 | 17,2 % |
| F | 241 | 70,54 % | | VENTURE | 5.719 | 14,8 % |
| G | 64 | 98,44 % | | | | |

---

## Auditoría de Calidad de Datos

* **Completitud:**
  * `loan_int_rate` tiene 3.116 nulos (9,6 %). La skill los imputa al punto medio y lo avisa en su salida.
  * `person_emp_length` tiene 895 nulos (2,7 %). No es entrada de la skill.
* **Valores atípicos:**
  * 7 filas con `person_age > 100` o `person_emp_length > 60` (máx. 144 años y 123 años de antigüedad). Son errores de origen; no afectan al score porque esas columnas no son entradas.
* **Duplicados:**
  * 165 filas idénticas en todas las columnas salvo `id`. Se conservan tal y como vienen en el dataset original.
* **Consistencia:**
  * `loan_grade` y `cb_person_default_on_file` solo contienen los valores esperados; la skill rechaza cualquier otro.

---

## Posibles Errores, Límites y Sesgos Identificados

1. **Crédito al consumo, no B2B:**
   * Son préstamos personales de 500 a 35.000 $. Las conclusiones no son directamente trasladables a facturas entre empresas sin recalibrar.
2. **Datos estáticos:**
   * Es una fotografía sin fechas: no permite calcular DSO, días de retraso ni evolución temporal. En producción haría falta una fuente actualizada (webhooks / cron jobs).
3. **Moneda única:**
   * Todos los importes están en una sola moneda ($). Operar en varias divisas exigiría una tabla de tipos de cambio.
4. **Sesgo de variables personales:**
   * Edad o vivienda pueden introducir discriminación si se usan para decidir. Por eso la skill solo usa variables financieras del préstamo y del historial de pago.
