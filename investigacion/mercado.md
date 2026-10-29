# Investigación de Mercado: Monitorización y Alerta Temprana de Riesgo Crediticio e Impagos


## 1. Análisis de Mercado y Oportunidad de Negocio
El incremento global de los tipos de interés y la volatilidad económica han apretado la liquidez de empresas y familias. En sectores como el SaaS, la Fintech y el crédito al consumo, la gestión tradicional del riesgo de crédito es predominantemente **reactiva**: las acciones de cobro o de revisión del crédito empiezan cuando un pago ya lleva entre 30 y 60 días en mora.

* **El problema real:** cuanto más se tarda en detectar el riesgo, más se degrada el capital circulante y más probable es que el impago acabe siendo irrecuperable (*write-off*).
* **La oportunidad:** pasar de una auditoría contable pasiva a un **mecanismo agéntico proactivo** que evalúe el riesgo con variables financieras e historial de pago antes de que se produzca el impago.

---

## 2. Soluciones Actuales en el Mercado
1. **ERP / módulos de contabilidad tradicionales (SAP, NetSuite, Holded, QuickBooks):**
   * *Mecanismo:* generan informes estáticos de antigüedad de deuda (*aging reports*).
   * *Limitación:* dependen 100 % de la revisión manual de analistas de crédito o contables.
2. **Plataformas de automatización de cobros (Chaser, HighRadius, Quadient/YayPay):**
   * *Mecanismo:* reglas deterministas simples (por ejemplo, "si la factura lleva más de 5 días vencida, enviar el email X").
   * *Limitación:* no contextualizan la situación global del deudor ni anticipan el riesgo antes del vencimiento.
3. **Burós de crédito y scoring externo (Experian, Dun & Bradstreet):**
   * *Mecanismo:* aportan puntuaciones crediticias macro o financieras externas.
   * *Limitación:* están desconectados de la operativa diaria y no prescriben qué acción tomar.

---

## 3. Matriz Comparativa de Competidores
| Solución / Enfoque | Tipo de análisis | Nivel de automatización | Adaptabilidad / Contexto | Capacidad agéntica |
| :--- | :--- | :--- | :--- | :--- |
| **ERP tradicional** | Descriptivo (pasado) | Manual / nulo | Muy baja | No |
| **Automatización de cobros (Chaser)** | Basado en reglas | Automatizado secuencial | Media (plantillas estáticas) | No |
| **Rating de crédito (Experian)** | Predictivo macro | Estático (feeds de datos) | Baja | No |
| **Nuestra solución agéntica** | **Prescriptivo y explicable** | **Agente con herramientas** | **Alta (SQL a demanda + skill)** | **Sí (Skill + MCP)** |

---

## 4. Limitaciones Actuales y Brecha de Innovación
1. **Fragmentación de datos:** los datos de crédito están aislados de las herramientas de análisis; consultar un segmento nuevo exige pedir un informe a otro equipo.
2. **Inflexibilidad en las acciones de cobro:** enviar correos genéricos a todos los deudores genera fricción y deteriora la relación comercial.
3. **Escasez de prescripción:** los dashboards informan del problema ("hay 50.000 $ en riesgo") pero no recomiendan la acción óptima: recordatorio, refinanciación en 3 cuotas o recobro.

---

## 5. Ventaja Competitiva de la Propuesta Agéntica
* **Acceso a datos vía MCP:** el agente consulta la base de datos en lenguaje natural mediante el MCP oficial de Supabase, en modo solo lectura.
* **Lógica garantizada (Skill):** el Score de Riesgo se calcula de forma determinista con una fórmula transparente y auditable, expuesta también como servidor MCP propio.
* **Respuestas proporcionales con control humano:** el agente propone la acción según la matriz de severidad; las acciones críticas requieren autorización humana.

---

## 6. Ajuste a los datos disponibles
La investigación inicial apuntaba a facturas B2B (DSO, días de vencimiento). No encontramos un dataset público y real con esas variables, así que trabajamos con el **Credit Risk Dataset de Kaggle** (32.581 préstamos con el resultado real de impago). El razonamiento de mercado se mantiene: detectar el riesgo antes del impago y prescribir la acción. Cambia la unidad de análisis: préstamo en lugar de factura. Ver [problema.md](problema.md) y [data/fuente.md](../data/fuente.md).
