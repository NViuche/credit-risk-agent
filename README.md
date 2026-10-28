# Conexión con MySQL local (XAMPP)

El proyecto se conecta a `bi_riesgo_crediticio` mediante un servidor MCP local. La configuración de [`.mcp.json`](./.mcp.json) permite que los clientes compatibles, incluido Copilot, inicien el servidor con el proyecto. phpMyAdmin sirve para administrar y consultar MySQL desde el navegador; no es el servidor de base de datos.

## Requisitos

- XAMPP instalado y el servicio **MySQL** iniciado desde el panel de control.
- `uvx` disponible en PATH. Se puede comprobar con `uvx --version`.
- La base `bi_riesgo_crediticio` creada en MySQL.

La configuración usa `127.0.0.1:3306` por defecto. Si XAMPP muestra otro puerto, establece `MYSQL_PORT` con ese valor antes de iniciar VS Code.

## Crear un usuario de solo lectura

En phpMyAdmin, abre la pestaña SQL y ejecuta lo siguiente como administrador. Sustituye `CAMBIA_POR_UNA_CLAVE_SEGURA` por una clave propia y no guardes esa clave en este proyecto:

```sql
CREATE USER 'mcp_riesgo_lectura'@'127.0.0.1'
  IDENTIFIED BY 'CAMBIA_POR_UNA_CLAVE_SEGURA';
GRANT SELECT, SHOW VIEW ON bi_riesgo_crediticio.*
  TO 'mcp_riesgo_lectura'@'127.0.0.1';
```

Si el usuario ya existe, cambia su clave con `ALTER USER` en lugar de volver a ejecutar `CREATE USER`. No configures el MCP con el usuario `root`.

## Iniciar VS Code con las credenciales

En PowerShell, desde la carpeta del proyecto, establece las variables y abre VS Code desde esa misma terminal:

```powershell
$env:MYSQL_USER = 'mcp_riesgo_lectura'
$env:MYSQL_PASSWORD = 'CAMBIA_POR_LA_CLAVE_QUE_CONFIGURASTE'
code .
```

Si VS Code ya estaba abierto, cierra todas sus ventanas antes de ejecutar `code .`, para que el proceso nuevo herede las variables. Las variables así establecidas duran mientras exista esa terminal. Para usarlas en futuras sesiones, guárdalas en las variables de entorno de usuario de Windows y reinicia VS Code; evita incluir credenciales en `.mcp.json` o en archivos versionados.

## Verificar la conexión

1. Confirma que MySQL está iniciado en XAMPP y que el puerto coincide.
2. En VS Code, abre la sección **MCP Servers** y reinicia o inicia `mysql-riesgo-crediticio` si se solicita.
3. En una sesión de Copilot, pide: «Usa `mysql-riesgo-crediticio` para listar las tablas de `bi_riesgo_crediticio` y describir sus columnas. No ejecutes cambios».
4. Comprueba que Copilot devuelve las tablas existentes. Para analizar registros, consulta primero el esquema y confirma que los datos no contienen información sensible que no se deba compartir con el modelo.

El servidor MCP ofrece herramientas SQL; el permiso `SELECT` del usuario configurado es lo que impide que esas herramientas inserten, actualicen o eliminen datos. La base actual es de prueba: revisa sus tablas y columnas antes de definir consultas de riesgo crediticio.
