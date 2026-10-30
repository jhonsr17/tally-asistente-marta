# Permisos y estado de la entrega

## Disponible en el paquete

- Adaptador MCP de lectura para listar US → MX, consultar una ficha, listar hilos y abrir un hilo devuelto por ese índice.
- Borradores redactados en el chat.
- Conexión HTTPS autenticada al backend; requiere configuración local y acceso autorizado.

## Pendiente, no activado

- Credencial individual/revocable para el agente y restricción US → MX aplicada en servidor.
- Edición de etapas, responsables, pausas, bloqueos, notas, cierres y reaperturas con bitácora.
- Lectura directa de transcripciones y creación de borradores Gmail mediante API aprobada.
- Automatización permanente de seguimiento, independiente del equipo local.

No usar una API key global, la llave DWD ni una contraseña de base de datos. El permiso de lectura entre buzones se resuelve en el backend y su lista configurada. Clonar no transmite permisos.

El adaptador limita sus rutas, pero no reduce los permisos de una credencial amplia fuera de él. La restricción de seguridad debe residir en el servidor. El acceso a un hilo exige además pertenencia al lead validada por el backend.

El índice puede ser parcial, tener caché o límites de búsqueda: no equivale a todos los correos existentes. Si una lectura falla, señalar la cobertura faltante.

Algunas rutas GET existentes pueden calcular/cachar datos o clasificar adjuntos como parte de su implementación. El adaptador no ejecuta mutaciones comerciales ni permite HTTP/SQL arbitrario; no promete cero escrituras internas de caché en el backend.
