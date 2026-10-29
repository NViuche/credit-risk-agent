# Reflexión del Proyecto: CreditGuard AI

## Contexto: hechos del proyecto
- **Qué construimos:** un agente (Claude Code) que consulta 32.581 préstamos reales en Supabase por MCP y los puntúa con una skill propia. Además, un servidor MCP propio hecho con el SDK oficial, un backend y un frontend en Streamlit. Las acciones críticas requieren autorización humana.
- **Resultado:** el score separa bien el riesgo (8,2 % de impago en BAJO frente a 72,1 % en CRÍTICO; AUC 0,793). Las 9 pruebas obligatorias están aprobadas.
- **Bloqueos reales que tuvimos:**
  - La primera versión del agente y de la skill describía tablas (`facturas`, `clientes`, `metricas_riesgo`) que no existían en la base de datos.
  - El MCP de Supabase se quedaba en "Pending approval" porque faltaba `.claude/settings.local.json`.
  - Los nombres de archivo con ñ, tildes y espacios se rompían en git.
  - La Data API de Supabase devolvía `Invalid API key` hasta que pusimos la clave Publishable correcta.
  - La versión 2.x del SDK de MCP había cambiado nombres respecto a la documentación que conocíamos.
- **Decisiones clave:**
  - Adaptar el agente al dataset real en lugar de inventar tablas B2B.
  - Usar una fórmula explicable en lugar de un modelo de caja negra.
  - Excluir variables personales (edad, vivienda) del score.
  - Configurar el MCP en solo lectura.

---

## 1. Reflexión individual

### Integrante: Roberto Mario Brochero López
1. **¿Qué he aprendido?**
   ✍️
2. **¿Qué me llevo y cómo lo aplicaré?**
   ✍️
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   ✍️
4. **¿Qué he aportado al equipo?**
   ✍️
5. **¿Qué haría diferente la próxima vez?**
   ✍️

### Integrante: Sofía Montero Jara
1. **¿Qué he aprendido?**
   Que otra pagina que es similar a supabase que se llama neon y que se puede utilizar gratis
2. **¿Qué me llevo y cómo lo aplicaré?**
   Me llevo que que se pueden conseguir bases de datos confiables en kaggle, también como hacer la vinculación con neon y visual studios, lo puedo aplicar para futuros proyectos de análisis de datos y para practicar casos de GitHub
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   Nos bloqueamos con la unión de supabase con Visual Code nos da error, primero empezamos a buscar otras opciones como neon pero mientras se ejecutaba la conexión con neon un compañero reviso el error y nos ayudó a solucionar
4. **¿Qué he aportado al equipo?**
   He aportado creando las estructuras en mi gemini, para solo ejecutarlas en claude y asi ahorrar tokens
5. **¿Qué haría diferente la próxima vez?**
   ✍️

### Integrante: Santiago Nicolás Viuche Pinilla
1. **¿Qué he aprendido?**
   ✍️
2. **¿Qué me llevo y cómo lo aplicaré?**
   ✍️
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   ✍️
4. **¿Qué he aportado al equipo?**
   ✍️
5. **¿Qué haría diferente la próxima vez?**
   ✍️

---

## 2. Reflexión colectiva
1. **¿Qué hemos aprendido trabajando juntos?**
   ✍️
2. **¿Qué nos llevamos de la experiencia?**
   ✍️
3. **¿Qué bloqueos tuvimos y cómo los resolvimos?**
   ✍️
4. **¿Cómo hemos decidido, escuchado y cuestionado a la IA?**
   ✍️
5. **¿Qué haríamos distinto si empezáramos de nuevo?**
   ✍️

---

## 3. Compromisos del equipo
| | Compromiso |
| :--- | :--- |
| **Mantener** | ✍️ |
| **Cambiar** | ✍️ |
| **Experimentar** | ✍️ |
