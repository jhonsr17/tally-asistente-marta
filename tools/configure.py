"""Configurador interactivo: no lee ni copia accesos del workspace de Jhon."""
import getpass
import json
import os
from client import config_path, validate_url


def main():
    print('Configura únicamente el acceso individual aprobado por el equipo de Tally.')
    target = config_path()
    if target.exists() and input('Ya hay una conexión. ¿Reemplazarla? [s/N] ').strip().lower() != 's':
        return
    url = validate_url(input('URL HTTPS raíz del backend: ').strip())
    token = getpass.getpass('Token individual (oculto): ').strip()
    if not token or '\n' in token or '\r' in token:
        raise ValueError('Token vacío o inválido.')
    target.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as handle:
        json.dump({'url': url, 'token': token}, handle)
    print('Conexión local guardada fuera del repo. No se ha probado acceso ni ampliado permisos.')


if __name__ == '__main__':
    main()
