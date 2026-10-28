# Diagrama de Flujo del Sistema Agéntico: Credit Risk & Default Intelligence

```mermaid
graph TD
    %% Roles y Capas
    subgraph CAPA_INTERFAZ [Capa de Interfaz & Usuario]
        UI[Usuario / Analista Financiero]
    end

    subgraph CAPA_ORQUESTACION [Capa de Inteligencia Agéntica]
        AGENT[Agente Coordinador de Riesgo]
        PROMPT[Instrucciones & Contexto de Negocio]
        AGENT --- PROMPT
    end

    subgraph CAPA_HERRAMIENTAS [Protocolo de Herramientas & Logica]
        DATA[Acceso a datos - pendiente de definir]
        SKILL[Skill Propia: Risk Score Engine]
    end

    subgraph CAPA_DATOS [Capa de Persistencia]
        DB[(Fuente de datos - pendiente de definir)]
    end

    subgraph CAPA_SALIDA [Resultados & Entregables BI]
        OUT_DASHBOARD[Informe Ejecutivo & KPIs]
        OUT_ACTION[Acción de Mitigación / Plan de Recobro]
    end

    %% Flujo de Ejecución Sequencial
    UI -->|1. Consulta: "Analiza el riesgo de impago del mes"| AGENT
    
    AGENT -->|2. Identifica necesidad de datos| DATA
    DATA -.->|Conexión por definir| DB
    DATA -->|3. Entrega datos estructurados| AGENT