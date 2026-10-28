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
        MCP[Servidor MCP MySQL - Herramientas SQL de solo lectura]
        SKILL[Skill Propia: Risk Score Engine]
    end

    subgraph CAPA_DATOS [Capa de Persistencia]
        DB[(MySQL local de XAMPP: bi_riesgo_crediticio)]
    end

    subgraph CAPA_SALIDA [Resultados & Entregables BI]
        OUT_DASHBOARD[Informe Ejecutivo & KPIs]
        OUT_ACTION[Acción de Mitigación / Plan de Recobro]
    end

    %% Flujo de Ejecución Sequencial
    UI -->|1. Consulta: "Analiza el riesgo de impago del mes"| AGENT
    
    AGENT -->|2. Identifica necesidad de datos| MCP
    MCP -->|3. Consulta SQL: SELECT facturas + métricas| DB
    DB -->|4. Retorna registros de facturas y clientes| MCP
    MCP -->|5. Entrega datos estructurados| AGENT