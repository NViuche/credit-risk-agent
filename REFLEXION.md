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
   He aprendido que existen alternativas a Supabase, como Neon, que ofrece una opción para trabajar con bases de datos de forma gratuita y online, además de herramientas como Obsidian. Esto me ha permitido conocer otras herramientas que podemos utilizar en nuestros proyectos de análisis de datos de forma más accesible, ya que permiten alojar las bases de datos online, lo que facilita compartirlas y hace posible trabajar con ellas desde cualquier lugar.
2. **¿Qué me llevo y cómo lo aplicaré?**
   Me llevo una nueva herramienta muy potente que brinda la posibilidad de crear agentes personalizados para resolver tareas específicas sin necesidad de ser experto en lenguajes de programación.
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   La conexión de las bases de datos fue bastante difícil, sobre todo al momento de conectar las credenciales o conceder permisos. Logré superar estos obstáculos con ayuda de la IA: preguntando cómo resolver esto o aquello, logré continuar con el proceso y utilizar herramientas que nunca había utilizado.
4. **¿Qué he aportado al equipo?**
   He contribuido con ideas y desarrollando tareas específicas que fuimos repartiendo durante el desarrollo del ejercicio.
5. **¿Qué haría diferente la próxima vez?**
   Buscaría la forma de dividir el trabajo de modo que pueda realizarse desde diferentes ordenadores de forma simultánea, combinando los desarrollos de cada uno en un único resultado. Seguramente lo haría con herramientas de control de versiones, donde cada uno puede tomar el proyecto desde el mismo punto y luego unificar los avances.

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
   He aprendido a integrar bases de datos alojadas en la nube, específicamente Supabase, con VS Code y a trabajar con el LLM de Claude. También he aprendido el uso puntual de archivos JSON para el llamado de credenciales y el posterior manejo de las bases de datos.
2. **¿Qué me llevo y cómo lo aplicaré?**
   Me llevo el conocimiento de la conectividad entre VS Code y Supabase, así como haber aprendido a habilitar MCP desde VS Code y a manejarlo tras reiniciar la ventana.
3. **¿Dónde me he bloqueado y cómo lo he afrontado?**
   Me bloqueé en la implementación de Supabase. Como era una herramienta y un propósito (el llamado a una base de datos en la nube) que no había usado antes en VS Code, se presentaron bastantes trabas, desde la subida de la base de datos hasta la conectividad con VS Code, que finalmente se consiguió.
4. **¿Qué he aportado al equipo?**
   Aporté el montaje del agente en VS Code y el posterior trabajo en Claude, a la par con el apoyo de Gemini del equipo, optimizando tokens y evitando reprocesos, así como la organización del proyecto y del agente y su posterior subida a GitHub.
5. **¿Qué haría diferente la próxima vez?**
   Verificaría antes la documentación, las instrucciones del LLM y los pasos para la implementación de complementos.

---

## 2. Reflexión colectiva
1. **¿Qué hemos aprendido trabajando juntos?**
   Hemos aprendido a repartir el trabajo según lo que cada herramienta y cada persona hacía mejor: cada integrante asumió tareas concretas que fuimos repartiendo durante el desarrollo. Preparábamos estructuras e instrucciones en Gemini y las ejecutábamos en Claude, lo que nos ayudó a optimizar tokens y evitar reprocesos. También aprendimos que, cuando aparece un bloqueo, conviene explorar alternativas sin dejar de investigar la causa del problema original. Así ocurrió con la conexión entre Supabase y VS Code: una parte del equipo probaba Neon mientras otra resolvía el error.
2. **¿Qué nos llevamos de la experiencia?**
   Nos llevamos cómo construir un sistema agéntico completo con datos reales: buscar un dataset fiable en Kaggle, cargarlo en una base de datos en la nube, conectarla con VS Code y habilitar MCP para que el agente la consulte. Además, conocimos alternativas como Neon, que facilitan compartir y trabajar las bases de datos desde cualquier lugar, y aprendimos a manejar las credenciales de forma segura, fuera del repositorio. También descubrimos que es posible crear agentes personalizados para tareas específicas sin ser expertos en programación. Son conocimientos que podemos aplicar en futuros proyectos de análisis de datos.
3. **¿Qué bloqueos tuvimos y cómo los resolvimos?**
   El principal fue conectar Supabase con VS Code: desde la carga de la base de datos hasta las credenciales, los permisos y la aprobación del MCP, que se quedaba pendiente por falta de un archivo de configuración. Lo resolvimos revisando el error mientras explorábamos Neon como plan alternativo, y apoyándonos en la IA para entender cada paso. Otro bloqueo fue que la primera versión del agente describía tablas que no existían en la base de datos; lo detectamos al conectar el MCP y rediseñamos la skill sobre los datos reales. También corregimos nombres de archivo con caracteres especiales que se rompían en git y una clave de API que no era válida.
4. **¿Cómo hemos decidido, escuchado y cuestionado a la IA?**
   Usamos la IA como apoyo, no como fuente de verdad. Nos ayudó a desbloquearnos, preguntándole cómo resolver problemas concretos de credenciales y permisos, pero no dimos por buenas sus respuestas sin comprobarlas. Cuando propuso tablas que no existían, adaptamos el agente al dataset real en lugar de inventar datos. Contrastamos sus cifras con consultas directas a la base de datos, y así detectamos y corregimos errores, como un recuento equivocado de pruebas. Tampoco le dejamos aprobarse permisos por su cuenta, y las decisiones críticas de cobro siempre quedan en manos de una persona. Combinar Gemini y Claude nos obligó, además, a revisar lo que proponía cada uno antes de ejecutarlo.
5. **¿Qué haríamos distinto si empezáramos de nuevo?**
   Organizaríamos el trabajo para avanzar en paralelo desde varios ordenadores, en lugar de concentrar el desarrollo en uno solo; así, un bloqueo técnico no detendría todo el proyecto. Para ello usaríamos el control de versiones desde el principio, de modo que cada uno parta del mismo punto y luego unifiquemos los avances. También revisaríamos antes la documentación, las instrucciones del LLM y los pasos de instalación de cada complemento, y miraríamos los datos reales antes de diseñar el agente.

---

## 3. Compromisos del equipo
| | Compromiso |
| :--- | :--- |
| **Mantener** | El reparto de trabajo entre Gemini y Claude para optimizar tokens, y la costumbre de validar cada cifra contra los datos reales. |
| **Cambiar** | Trabajar en paralelo desde varios ordenadores con control de versiones (Git), y revisar la documentación y los requisitos de cada herramienta antes de implementarla. |
| **Experimentar** | Probar alternativas como Neon desde el inicio y comparar opciones antes de elegir la base de datos, y crear nuevos agentes personalizados para otras tareas de análisis. |
