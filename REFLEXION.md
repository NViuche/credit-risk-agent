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
   He aprendido que existen alternativas a Supabase, como Neon, que ofrece una opción para trabajar con bases de datos de forma gratuita. Esto me ha permitido conocer otras herramientas que podemos utilizar en nuestros proyectos de análisis de datos.
2. **¿Qué me llevo y cómo lo aplicaré?**
   Me llevo el aprendizaje de cómo encontrar bases de datos útiles y confiables en Kaggle, así como el proceso de conexión de Neon con Visual Studio Code. Estos conocimientos podré aplicarlos en futuros proyectos de análisis de datos y en la práctica de casos disponibles en GitHub.
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   Nos encontramos con un problema al intentar conectar Supabase con Visual Studio Code, ya que se producía un error. Inicialmente, buscamos alternativas, como Neon, para poder continuar con el proyecto. Mientras intentábamos establecer la nueva conexión, un compañero revisó el error original y nos ayudó a solucionarlo. Esta experiencia nos enseñó la importancia de explorar otras opciones sin dejar de investigar la causa del problema inicial.
4. **¿Qué he aportado al equipo?**
   He contribuido preparando las estructuras e instrucciones en Gemini para ejecutarlas posteriormente en Claude, con el objetivo de optimizar el uso de tokens. También he buscado bases de datos en Kaggle que pudieran ser útiles para el proyecto y he ayudado a mantener el seguimiento de las tareas, identificando qué actividades estaban pendientes para procurar que no quedara ninguna sin completar.
5. **¿Qué haría diferente la próxima vez?**
   La próxima vez organizaría el trabajo para que pudiéramos avanzar desde ambos ordenadores en paralelo, en lugar de concentrar todo el desarrollo en uno solo. Cuando surgió el problema de conexión entre Supabase y Visual Studio Code, perdimos bastante tiempo intentando resolverlo y el avance del proyecto se detuvo. Si hubiéramos trabajado simultáneamente en ambos equipos, podríamos haber continuado con otras tareas mientras solucionábamos el error, aprovechando mejor el tiempo y reduciendo los bloqueos.

### Integrante: Santiago Nicolas Viuche Pinilla
1. **¿Qué he aprendido?**
   Integrar bases de datos subidas en la nube con VS y trabajando con el LLM de Claude, específicamente con Supabase, así aprender uso puntual del archivos JSON para el llamado de credenciales y posterior manejo de bases de datos
2. **¿Qué me llevo y cómo lo aplicaré?**
   Me llevo el conocimiento de la conectividad entre VS con Supabase, así como haber aprendido a habilitar MCP desde VS y posterior maneja tras reinicio de ventanas.
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   En la implementación de Supabase, debido a que era una herramienta y propósito (llamado a BD en la nube) que no había usado antes en VS, por lo que presento bastantes trabas desde la subida de la BD hasta la conectividad con VS, que se termino consiguiendo.
4. **¿Qué he aportado al equipo?**
   Aporte montar el agente en VS y posterior trabajo en Claude a la par con el apoyo de Gemini del equipo, optimizando tokens y evitando reprocesos, así como la organización del proyecto/agente y posterior subida a GitHub
5. **¿Qué haría diferente la próxima vez?**
   Verificar documentación, instrucciones del LLM y pasos para la implementación de complementos.

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
