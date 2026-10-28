### Diccionario de Datos

#### Tabla: `clientes`

| Columna | Tipo | Descripción | Restricciones |
| :--- | :--- | :--- | :--- |
| `cliente_id` | `VARCHAR(10)` | Identificador único del cliente | Primary Key |
| `nombre_empresa` | `VARCHAR(100)` | Nombre comercial de la empresa | NOT NULL |
| `sector` | `VARCHAR(50)` | Sector de actividad comercial | NOT NULL |
| `limite_credito` | `DECIMAL(10,2)` | Límite máximo de crédito asignado (\$) | Default 0.00 |
| `fecha_alta` | `DATE` | Fecha de registro en la plataforma | NOT NULL |

#### Tabla: `facturas`

| Columna | Tipo | Descripción | Restricciones |
| :--- | :--- | :--- | :--- |
| `factura_id` | `VARCHAR(10)` | Identificador único de factura | Primary Key |
| `cliente_id` | `VARCHAR(10)` | Relación con la cuenta del cliente | Foreign Key (`clientes`) |
| `monto` | `DECIMAL(10,2)` | Importe total de la factura (\$) | NOT NULL |
| `fecha_emision` | `DATE` | Fecha de emisión de la factura | NOT NULL |
| `fecha_vencimiento` | `DATE` | Fecha límite de pago acordada | NOT NULL |
| `estado` | `ENUM` | Estado financiero (`PAGADA`, `PENDIENTE`, `VENCIDA`) | Default `PENDIENTE` |
| `dias_retraso_pago` | `INT` | Días transcurridos tras vencimiento | Default 0 |

#### Tabla: `metricas_riesgo`

| Columna | Tipo | Descripción | Restricciones |
| :--- | :--- | :--- | :--- |
| `cliente_id` | `VARCHAR(10)` | Relación con el cliente | Primary Key, Foreign Key |
| `dso_historico` | `INT` | Días promedio de cobro histórico (DSO) | Default 0 |
| `porcentaje_credito_usado` | `DECIMAL(5,2)` | Porcentaje del límite consumido (%) | Default 0.00 |
| `score_buro_credito` | `INT` | Puntuación de crédito externa (300-850) | Default 600 |
| `incidentes_pago_ultimos_6m` | `INT` | Recibos devueltos en los últimos 6 meses | Default 0 |

---

## 4. Auditoría de Calidad de Datos

* **Completitud:**
  * Durante el proceso de ETL (`data/cargar_datos.py`), se aplican reglas de filtrado para eliminar valores nulos (`NaN` o `NULL`) en columnas críticas como montos o estados.
* **Integridad Referencial:**
  * Garantizada mediante claves foráneas con restricciones `ON DELETE CASCADE ON UPDATE CASCADE` en InnoDB, evitando la existencia de facturas o métricas huérfanas sin cliente asignado.
* **Consistencia de Datos:**
  * Los importes y ratios porcentuales se normalizan a dos decimales (`DECIMAL(10,2)` y `DECIMAL(5,2)`).
  * Los estados de factura están limitados por un tipo estricto `ENUM` para evitar incoherencias en las consultas SQL del agente.

---

## 5. Posibles Errores, Límites y Sesgos Identificados

1. **Sesgo de Muestra Unilateral:**
   * Al mapear datos de crédito al consumo hacia un entorno B2B, los montos promedio representan operaciones medianas (\$1,000 - \$35,000). Para grandes corporaciones B2B con facturas de millones de dólares, la escala debe ajustarse.
2. **Estacionalidad y Datos Estáticos:**
   * El dataset en su versión inicial es estático (fotografía temporal). En un entorno de producción real, las métricas de uso y estado de facturas deben actualizarse mediante un flujo en tiempo real (webhooks/cron jobs).
3. **Manejo de Monedas Múltiples:**
   * La estructura actual asume una única moneda base (\$ / €). Si la empresa opera en múltiples divisas, se requeriría una tabla adicional de tipos de cambio.