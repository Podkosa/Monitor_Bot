import logging, sys, pathlib
import aiohttp, yaml
from fastapi.logger import logger

from . import default_setters

class SettingsError(Exception):
    pass

### Logging ###
logger.handlers = [logging.StreamHandler(sys.stdout)]
logger.setLevel(logging.INFO)

### General ###
WORK_DIR = pathlib.Path()
yml: dict = yaml.safe_load(open(WORK_DIR / 'settings.yml', mode='r'))
if yml is None:
    raise SettingsError('Could not parse settings.yml.')

API_KEY = yml.pop('api_key', None)
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=yml.get('request_timeout', 10))
DTTM_FORMAT = yml.get('dttm_format', '%Y-%m-%d %H:%M:%S')

### Watchdog ###
WATCHDOG = yml.get('watchdog', {})

### Checkers ###
CHECKERS = yml.get('checkers', {})
if not CHECKERS:
    raise SettingsError('At least one checker must be defined')

for checker, conf in CHECKERS.items():
    if not conf:
        raise SettingsError(f'{checker} checker has incorrect value: {conf}')
    if not conf.get('servers'):
        raise SettingsError(f'{checker} checker has no servers defined')
    defaults = WATCHDOG.get('default', {}).copy()                                   # Watchdog level defaults
    defaults.update(conf.get('default', {}))                                        # Checker level defaults
    for host, params in conf['servers'].items():
        if params is None:
            params = conf['servers'][host] = {}
        params.setdefault('handlers', defaults.get('handlers'))
        params.setdefault('cycle', defaults.get('cycle', 300))
        params.setdefault('protocol', defaults.get('protocol', 'https'))
        getattr(default_setters, checker, lambda *args: None)(params, defaults)     # Server level defaults

### Handlers ###
HANDLERS = yml.get('handlers', {})
if not HANDLERS:
    raise SettingsError('At least one handler must be defined')

### Integrations ###
INTEGRATIONS = yml.get('integrations', {})
