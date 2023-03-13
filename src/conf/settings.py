import logging, sys, pathlib
import yaml
from fastapi.logger import logger

from . import default_setters

class SettingsError(Exception):
    pass


### General ###
WORK_DIR = pathlib.Path()
yml: dict = yaml.safe_load(open(WORK_DIR / 'settings.yml', mode='r'))
if yml is None:
    raise SettingsError('Could not parse settings.yml.')

API_KEY = yml.pop('api_key', None)
REQUEST_TIMEOUT = yml.get('request_timeout', 10)
SSH_TIMEOUT = yml.get('ssh_timeout', REQUEST_TIMEOUT)
SSH_PASSPHRASE = yml.get('ssh_passphrase')
DTTM_FORMAT = yml.get('dttm_format', '%Y-%m-%d %H:%M:%S')

### Logging ###
logger.handlers = [logging.StreamHandler(sys.stdout)]
LOGGER_LEVEL = yml.get('logger_level', 'info')
__level_mapping__ = logging.getLevelNamesMapping()
if LOGGER_LEVEL.upper() not in __level_mapping__:
    raise SettingsError(f'Incorrect value {LOGGER_LEVEL} for logger_level')
logger.setLevel(__level_mapping__.get(LOGGER_LEVEL.upper()))  # type: ignore

### Watchdog ###
WATCHDOG = yml.get('watchdog', {})

### Checkers ###
CHECKERS = yml.get('checkers', {})
if not CHECKERS:
    raise SettingsError('At least one checker must be defined')

SHH_DEPENDENT_CHECKERS = {'docker'}

checkers_defaults = CHECKERS.pop('default', {}) or {}                               # Top level defaults
for checker, conf in CHECKERS.items():
    if not conf:
        raise SettingsError(f'{checker} checker has incorrect value: {conf}')
    if not conf.get('servers'):
        raise SettingsError(f'{checker} checker has no servers defined')
    if checker in SHH_DEPENDENT_CHECKERS and not pathlib.Path('/root/.ssh').exists():
        raise SettingsError(f'{checker} checker is defined, but /root/.ssh directory is not found. Make sure to mount it through a volume.')
    defaults = checkers_defaults.copy()
    defaults.update(conf.get('default', {}))                                        # Checker level defaults
    for host, params in conf['servers'].items():
        if params is None:
            params = conf['servers'][host] = {}
        params.setdefault('cycle', defaults.get('cycle', 300))
        params.setdefault('handlers', defaults.get('handlers'))
        params.setdefault('protocol', defaults.get('protocol', 'https'))
        params.setdefault('back_to_normal', defaults.get('back_to_normal', False))
        params.setdefault('back_to_normal_cycle', defaults.get('back_to_normal_cycle', params['cycle']))
        params.setdefault('not_normal_for', defaults.get('not_normal_for', 1))
        getattr(default_setters, checker, lambda *args: None)(params, defaults)     # Server level defaults

### Handlers ###
HANDLERS = yml.get('handlers', {})
if not HANDLERS and WATCHDOG.get('integrated'):
    raise SettingsError('At least one handler must be defined to send alerts')

### Integrations ###
INTEGRATIONS = yml.get('integrations', {})

### Startup/shutdown ###
ON_STARTUP_HANDLERS = yml.get('on_startup_handlers', [])
for handler in ON_STARTUP_HANDLERS:
    if handler not in HANDLERS:
        raise SettingsError(f'On startup handler {handler} is not defined in handlers')
ON_SHUTDOWN_HANDLERS = yml.get('on_shutdown_handlers', [])
for handler in ON_SHUTDOWN_HANDLERS:
    if handler not in HANDLERS:
        raise SettingsError(f'On shutdown handler {handler} is not defined in handlers')
