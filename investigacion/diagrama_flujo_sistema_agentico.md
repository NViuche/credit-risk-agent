# Diagrama de Flujo del Sistema Agéntico: Credit Risk & Default Intelligence

```mermaid
graph TD
    subgraph CAPA_INTERFAZ [Usuario / Interfaz]
        UI_CLAUDE[Analista en Claude Code - lenguaje natural]
        UI_WEB[Frontend Streamlit - frontend/app.py]
    end

    subgraph CAPA_ORQUESTACION [Agente coordinador]
        AGENT[CreditGuard AI]
        PROMPT[AGENTS.md + agents/creditguard.md]
        AGENT --- PROMPT
    end

    subgraph CAPA_HERRAMIENTAS [Skill · MCP · Datos]
        SKILL[Skill credit-risk - skills/credit-risk]
        MCP_SB[MCP oficial Supabase: execute_sql]
        MCP_CR[MCP propio credit-risk - backend/mcp_server.py]
        DB[(Supabase PostgreSQL: public.credit_risk)]
    end

    subgraph CAPA_BACKEND [Backend -> Resultado BI]
        SERV[backend/servicio.py: consulta, puntúa, KPI]
        OUT[KPI, tabla priorizada y acciones]
        HUMAN{¿Score > 65?}
    end

    UI_CLAUDE -->|1. Petición| AGENT
    AGENT -->|2a. Preguntas abiertas| MCP_SB
    MCP_SB -->|SQL solo lectura| DB
    AGENT -->|2b. Análisis de cartera| MCP_CR
    MCP_CR --> SERV
    UI_WEB -->|1. Filtros y botón Analizar| SERV
    SERV -->|3. SELECT parametrizado, sesión read-only| DB
    SERV -->|4. Puntúa cada préstamo| SKILL
    SERV -->|5. KPI y acciones| OUT
    OUT --> HUMAN
    HUMAN -->|No: recordatorio o plan en 3 cuotas| OUT
    HUMAN -->|Sí: propuesta pendiente| UI_WEB
    UI_WEB -->|Analista autoriza| OUT
```

**Dos puntos de entrada, una sola lógica:** tanto el agente (vía el MCP propio) como el frontend llaman a `backend/servicio.py`, que es el único lugar donde se combinan datos, skill y KPI.
