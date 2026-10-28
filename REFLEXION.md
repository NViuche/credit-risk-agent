# Reflexión del Proyecto

> Plantilla con los hechos del proyecto ya anotados. Las valoraciones personales (marcadas con ✍️) las tiene que escribir el equipo.

## 1. Qué hemos construido
Un agente (CreditGuard AI, en Claude Code) que consulta una cartera real de 32.581 préstamos en Supabase por MCP y la puntúa con una skill propia (`credit-risk`). Después propone acciones de cobro según el riesgo. Las acciones críticas requieren autorización humana.

## 2. Decisiones clave y por qué
- **Supabase en lugar de MySQL local:** el MCP oficial de Supabase permite al agente consultar la base de datos sin servidor propio y en modo solo lectura.
- **Adaptar el agente al dataset real en lugar de crear tablas B2B sintéticas:** con el tiempo disponible, priorizamos que el 100 % de las cifras saliera de datos reales.
- **Skill determinista y explicable:** una fórmula con 4 factores ponderados, en lugar de un modelo de machine learning, para que cada score se pueda explicar a negocio.
- **Excluir variables personales (edad, vivienda):** para no basar decisiones de cobro en rasgos de la persona.

## 3. Qué ha funcionado
- La skill ordena bien el riesgo: 8,2 % de impago en BAJO frente a 72,1 % en CRÍTICO (AUC 0,793).
- ✍️ …

## 4. Qué no ha funcionado / dificultades
- La primera versión de la skill y del agente describían tablas (`facturas`, `clientes`, `metricas_riesgo`) que no existían en la base de datos. Lo detectamos al conectar el MCP y lo rediseñamos.
- Nombres de archivo con "ñ", tildes y espacios se rompían en git entre ordenadores. Los renombramos.
- La conexión por Data API falla por la clave (`Invalid API key`).
- ✍️ …

## 5. Límites del resultado
- Son préstamos al consumo, no facturas B2B: no hay DSO ni fechas de vencimiento.
- Los pesos de la fórmula son de criterio experto; la mayoría de impagos (65 %) cae en MODERADO, no en CRÍTICO.
- ✍️ …

## 6. Qué haríamos con más tiempo
- Calibrar los pesos con regresión logística y comparar con la fórmula actual.
- Crear las tablas B2B (`clientes`, `facturas`) marcando como sintético lo derivado.
- ✍️ …

## 7. Uso de IA en el proyecto
✍️ Cómo usamos Claude / otros asistentes, qué revisamos a mano y qué aprendimos.

## 8. Aprendizajes individuales
✍️ Una o dos frases por integrante.
