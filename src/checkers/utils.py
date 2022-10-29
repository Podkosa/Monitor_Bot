import asyncio

from conf import settings
import checkers, handlers
from checkers.abstract import Checker


def get_checker_cls(checker_name: str) -> type[Checker]:
    if checker_name not in settings.CHECKERS:
        raise settings.SettingsError(f'Checker {checker_name} is not defined in settings')
    return getattr(checkers, f'{checker_name.capitalize()}Checker')

def get_loaded_checkers() -> tuple[Checker]:
    """Loads, caches and returns checker instances."""
    if not checkers.__loaded_checkers__:
        checkers.__loaded_checkers__ = tuple(get_checkers_from_settings())
    return checkers.__loaded_checkers__

def get_checkers_from_settings(include_handlers=True, **kwargs) -> list[Checker]:
    _checkers = []
    for checker_name, conf in settings.CHECKERS.items():
        Checker_cls = get_checker_cls(checker_name)
        server: str
        params: dict
        for server, params in conf['servers'].items():
            params = params.copy()
            handler_names = params.pop('handlers')
            if include_handlers:
                if not handler_names:
                    raise settings.SettingsError(f'No handlers defined for {checker_name} checker')
                params['handlers'] = [handlers.get_handler_cls(handler_name)() for handler_name in handler_names]
            params.update(kwargs)
            checker = Checker_cls(host=server, **params)
            _checkers.append(checker)
    return _checkers

async def monitor():
    """Start full monitoring"""
    await asyncio.gather(*(checker.monitor() for checker in get_loaded_checkers()))
    # As of 29.10.2022 `async with asyncio.TaskGroup` doesn't seem to be working when Watchdog is started as a script.
    # Never get's to execute anything from the `async with` body. Possible Python 3.11 bug, further investigation required.

async def full_check():
    """Run all checks from settings.CHECKERS"""
    _checkers = get_checkers_from_settings(include_handlers=False, include_normal=True)
    return await asyncio.gather(*(checker.check() for checker in _checkers))
