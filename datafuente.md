# Documentación del Dataset y Calidad de Datos

## 1. Fuente y Origen de los Datos
* **Nombre del Dataset Original:** Credit Risk Dataset.
* **Fuente:** Kaggle (público / open data).
* **Entorno de Despliegue:** Supabase (PostgreSQL gestionado).
* **Contexto de Dominio:** Adaptación B2B/Fintech para evaluar la morosidad, capacidad crediticia y días de mora acumulados en la cartera de cobros.

---

## 2. Licencia y Términos de Uso
* **Tipo de Licencia:** CC0: Public Domain / Open Data License.
* **Uso Permitido:** Libre para investigación, desarrollo académico, prototipado y evaluaciones tecnológicas (Hackathons).
* **Privacidad y GDPR/LOPD:** El conjunto de datos no contiene datos personales identificables (PII). Todos los registros están anonimizados y mapeados con identificadores sintéticos de cliente (`CLI-001`, `CLI-002`, etc.).

---

## 3. Estructura de la Base de Datos (Modelo Relacional)

La base de datos relacional `bi_riesgo_crediticio` consta de tres tablas interconectadas mediante claves foráneas:

```text
┌───────────────────────────┐         ┌───────────────────────────┐
│ clientes                  │         │ facturas                  │
├───────────────────────────┤         ├───────────────────────────┤
│ PK cliente_id             │◄────┬───┤ FK cliente_id             │
│    nombre_empresa         │     │   │ PK factura_id             │
│    sector                 │     │   │    monto                  │
│    limite_credito         │     │   │    fecha_emision          │
│    fecha_alta             │     │   │    fecha_vencimiento      │
└───────────────────────────┘     │   │    estado                 │
                                  │   │    dias_retraso_pago      │
                                  │   └───────────────────────────┘
┌───────────────────────────┐     │
│ metricas_riesgo           │     │
├───────────────────────────┤     │
│ PK,FK cliente_id          ├─────┘
│    dso_historico          │
│    porcentaje_credito     │
│    score_buro_credito     │
│    incidentes_pago_6m     │
└───────────────────────────┘
```