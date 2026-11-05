# Asistente comercial de Marta

Instrucciones para trabajar con ventas US → MX desde Claude Code, conectado al MCP nativo de Tally 360 con la cuenta personal de Marta.

## Instalación

1. Aceptar la invitación a https://github.com/jhonsr17/tally-asistente-marta y clonar el repositorio. Si ya está clonado, actualizarlo con `git pull`.
2. Abrir Claude Code dentro de la carpeta del repositorio.
3. En la terminal de esa computadora, registrar el servidor:

```powershell
claude mcp add --scope user --transport http tally-360 https://web-production-8140b.up.railway.app/api/mcp
```

4. Dentro de Claude Code, escribir `/mcp`, seleccionar `tally-360` y **Authenticate**. Iniciar sesión en la página del 360 con la cuenta de Marta y completar la verificación que solicite.
5. Consultar `/mcp` para comprobar el estado y las herramientas disponibles.

Esta ruta no requiere Python ni copiar tokens. La sesión se guarda mediante el cliente, fuera del repositorio. No compartir contraseñas, tokens ni llaves de servicio.

Alternativa de configuración por proyecto: copiar `.mcp.example.json` a `.mcp.json` y autenticar desde `/mcp`. Elegir una sola forma de registrar `tally-360` para evitar duplicados. Si antes se configuró el servidor local `tally-ventas`, deshabilitarlo en la configuración donde se agregó; su token no sirve para el MCP nativo.

## Primera prueba con Marta

- Pedir «Busca una empresa y muéstrame su ficha con fuentes y fechas». Confirmar su identidad en la conexión.
- Buscar un lead US → MX y comprobar etapa y responsable contra la interfaz del 360.
- Para probar escritura, Marta debe pedir una nota concreta en ese lead. Verificar en el 360 el contenido y el autor. Consultar después la ficha para confirmar el resultado.
- Si no aparece una herramienta o hay un rechazo de permisos, registrar el mensaje y revisarlo con Alan/Dilson. No usar credenciales de otra persona.

## Capacidades y límites

El código y las guías actuales del backend contemplan búsqueda, contexto de empresa, ficha de leads, pendientes, notas y actualización de leads. Las herramientas expuestas dependen del rol y la versión desplegada. Esta publicación no verifica la conexión de Marta en producción.

La conexión hereda los permisos humanos de Marta. El límite exclusivo US → MX del agente aún requiere validación e implementación en servidor: las instrucciones del repositorio acotan su trabajo, pero no reducen los permisos técnicos de su cuenta.

Gmail crudo, envío de correos, lectura directa de transcripciones y campañas de Instantly requieren herramientas y permisos adicionales. No quedan activados al clonar o autenticar este MCP. Ver `docs/permisos-y-acciones.md`.

## Adaptador local anterior

`tools/`, `requirements.txt` y `tests/` conservan el prototipo de consulta REST anterior como referencia. No se utiliza en la instalación recomendada. No configurar un token MCP nativo en `tools/configure.py`: ese token solo es válido en `/api/mcp`, mientras el prototipo llama otras rutas.

Sus pruebas se ejecutan con `python -m unittest discover -s tests -v`; no validan el servidor remoto, OAuth ni los permisos reales de Marta.
