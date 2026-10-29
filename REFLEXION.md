# Reflexión del Proyecto: CreditGuard AI

> Las respuestas marcadas con ✍️ las escribe cada integrante o el equipo. Se valora la honestidad y el pensamiento crítico, no las respuestas perfectas.

## Contexto: hechos del proyecto (para apoyar la reflexión)
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

Copiar este bloque una vez por integrante.

### Integrante: ✍️ (nombre)
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

### Integrante: ✍️ (nombre)
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

## 2. Reflexión colectiva (acuerdo del equipo)
1. **¿Qué hemos aprendido trabajando juntos?**
   ✍️
2. **¿Qué nos llevamos de la experiencia?**
   ✍️
3. **¿Qué bloqueos tuvimos y cómo los resolvimos?**
   ✍️ *(Punto de partida: los bloqueos reales listados en el contexto.)*
4. **¿Cómo hemos decidido, escuchado y cuestionado a la IA?**
   ✍️ *(Ejemplos para debatir: la IA propuso tablas que no existían y lo detectamos al conectar el MCP; validamos sus cifras con SQL directo; rechazamos dejar que se autoaprobara permisos.)*
5. **¿Qué haríamos distinto si empezáramos de nuevo?**
   ✍️

---

## 3. Compromisos del equipo
| | Compromiso |
| :--- | :--- |
| **Mantener** | ✍️ |
| **Cambiar** | ✍️ |
| **Experimentar** | ✍️ |
