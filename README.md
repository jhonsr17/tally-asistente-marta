# Asistente comercial de Marta

Paquete local para Claude Code que consulta el contexto de ventas US → MX en Tally 360. Estado: prototipo de lectura; la conexión a producción requiere acceso individual aprobado.

## Instalación acompañada

1. Aceptar la invitación al repositorio privado https://github.com/jhonsr17/tally-asistente-marta y clonarlo. Abrir Claude Code dentro de la carpeta clonada.
2. Instalar Python 3.11 o superior. Desde la raíz del clon:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Alan/Dilson debe proporcionar el mecanismo de autenticación aprobado para Marta. No compartir claves de servicio ni tokens por chat. Todavía no se ha emitido la credencial restringida del agente.
4. Ejecutar el configurador, con la URL HTTPS del backend (sin /api al final) y el token individual autorizado:

```powershell
.\.venv\Scripts\python.exe tools\configure.py
```

Guarda la conexión fuera del repo: `%APPDATA%/TallyMarta/connection.json` en Windows. El token se guarda como archivo local en el perfil, no como almacén cifrado: usar únicamente credenciales individuales aprobadas; no sincronizarlo ni compartirlo. El servidor también admite `TALLY_360_URL` y `TALLY_360_TOKEN` como variables de entorno.

5. Copiar `.mcp.example.json` a `.mcp.json` (ignorado por Git). Cambiar `command` por la ruta absoluta a `.venv/Scripts/python.exe` y `args[0]` por la ruta absoluta a `tools/server.py` del clon. No añadir secretos al JSON.
6. Abrir Claude Code, revisar la configuración MCP y habilitar el servidor local. Sin conexión configurada, sus herramientas devuelven un error explicativo.

## Primera prueba

Pedir: «Busca una empresa en US → MX, lee sus hilos relevantes y dime qué pasó, qué falta y cuál es el siguiente paso, con fuentes y fechas». Validar con Marta contra el 360.

Esta versión expone `estado_conexion`, `listar_us_mx`, `consultar_lead`, `listar_hilos` y `leer_hilo`. No guarda borradores en Gmail, no envía mensajes, no mueve etapas y no accede directamente a la base.

Las instrucciones están en `CLAUDE.md`. El contexto general vive en `docs/`. El repo no incluye la carpeta original de tokens, archivos de clientes, dump de correo, video ni historia de Pipedrive.

## Verificación local

```powershell
python -m unittest discover -s tests -v
```

Las pruebas usan respuestas simuladas y no requieren producción. Falta validación de extremo a extremo con la autenticación aprobada y prueba desde la computadora de Marta.

## Accesos pendientes

Clonar este repositorio entrega instrucciones y herramientas, pero no concede acceso al 360, Gmail, Instantly ni a la base de datos. Alan/Dilson debe habilitar el acceso individual al backend antes de configurar la conexión.

La versión publicada consulta US → MX y sus hilos. La edición del pipeline, las transcripciones directas y la operación de campañas siguen pendientes de implementación y validación.
