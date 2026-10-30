"""Cliente restringido a consultas comerciales; sin credenciales embebidas."""
import json
import os
import re
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, build_opener, HTTPSHandler, HTTPRedirectHandler
from uuid import UUID


class AccessError(Exception):
    pass


def config_path():
    base = Path(os.environ.get('APPDATA') or (Path.home() / '.config'))
    return base / 'TallyMarta' / 'connection.json'


def validate_url(value):
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/')):
        raise AccessError('Usa la URL HTTPS raíz del backend, sin usuario, query ni ruta /api.')
    return value.rstrip('/')


def connection():
    url, token = os.environ.get('TALLY_360_URL'), os.environ.get('TALLY_360_TOKEN')
    if not (url and token):
        path = config_path()
        if not path.exists():
            raise AccessError('Conexión pendiente. Ejecuta tools/configure.py con el acceso aprobado.')
        data = json.loads(path.read_text(encoding='utf-8'))
        url, token = url or data.get('url'), token or data.get('token')
    if not url or not token:
        raise AccessError('Falta URL o token individual autorizado.')
    if any(c in token for c in ('\n', '\r')):
        raise AccessError('Token inválido.')
    return validate_url(url), token


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, transport=None):
        self.transport = transport or self._request

    def _request(self, path, params=None):
        url, token = connection()
        target = url + path + ('?' + urlencode(params) if params else '')
        req = Request(target, headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}, method='GET')
        opener = build_opener(NoRedirect(), HTTPSHandler(context=ssl.create_default_context()))
        try:
            with opener.open(req, timeout=30) as res:
                raw = res.read(5_000_001)
                if len(raw) > 5_000_000:
                    raise AccessError('Respuesta demasiado grande; reduce la consulta.')
                return json.loads(raw)
        except HTTPError as exc:
            code = exc.code
            raise AccessError({401: 'Sesión vencida o credencial inválida.',
                               403: 'Acceso denegado por el 360.',
                               404: 'Lead o hilo no disponible en este alcance.',
                               429: 'Límite de consultas; reintentar más tarde.'}.get(code, f'El 360 devolvió HTTP {code}.')) from None
        except (URLError, TimeoutError, json.JSONDecodeError):
            raise AccessError('No se pudo leer el 360. No se omite la validación TLS ni se muestran credenciales.') from None

    @staticmethod
    def lead_id(value):
        try:
            return str(UUID(value))
        except (ValueError, TypeError, AttributeError):
            raise AccessError('El lead_id debe ser el UUID devuelto por el 360.') from None

    def pipeline(self, query='', owner='', stage=''):
        params = {k: v for k, v in {'q': query, 'owner': owner, 'stage': stage}.items() if v}
        if any(not isinstance(v, str) or len(v) > 200 for v in params.values()):
            raise AccessError('Filtro inválido o demasiado largo.')
        return self.transport('/api/growth/pipelines/us_mx', params)

    def lead(self, lead_id):
        lead_id = self.lead_id(lead_id)
        data = self.transport(f'/api/growth/pipelines/us_mx/leads/{lead_id}')
        row = data.get('row') if isinstance(data, dict) else None
        if not isinstance(row, dict) or row.get('pipeline') != 'us_mx':
            raise AccessError('El 360 no confirmó pertenencia a US → MX.')
        return data

    def threads(self, lead_id):
        lead_id = self.lead_id(lead_id)
        self.lead(lead_id)
        return self.transport(f'/api/growth/leads/{lead_id}/threads')

    def thread(self, lead_id, thread_id, mailbox):
        lead_id = self.lead_id(lead_id)
        if not isinstance(thread_id, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,200}', thread_id):
            raise AccessError('thread_id inválido.')
        if not isinstance(mailbox, str) or len(mailbox) > 254:
            raise AccessError('mailbox inválido.')
        index = self.threads(lead_id)
        key = f'{mailbox}:{thread_id}'
        allowed = any((t.get('thread_id') == thread_id and t.get('mailbox') == mailbox)
                      or t.get('thread_key') == key or key in (t.get('alt_keys') or [])
                      for t in index.get('threads', []))
        if not allowed:
            raise AccessError('El hilo no figura en el índice autorizado del lead. No se abre un buzón arbitrario.')
        return self.transport(f'/api/growth/leads/{lead_id}/threads/{thread_id}', {'mailbox': mailbox})
