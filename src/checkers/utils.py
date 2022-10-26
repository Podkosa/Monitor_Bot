import asyncio
import settings, checkers, handlers


def get_checker_cls(checker_name: str):
    return getattr(checkers, f'{checker_name.capitalize()}Checker')

async def check_all():
    """Run all checks from settings.CHECKERS. Alert through handlers."""
    async with asyncio.TaskGroup() as tg:
        for checker_name, conf in settings.CHECKERS.items():
            Checker = checkers.get_checker_cls(checker_name)
            _handlers = [handlers.get_handlers_cls(handler)() for handler in conf['handlers']]
            for host, params in conf['servers'].items():
                tg.create_task(
                    Checker(handlers=_handlers, host=host, **params).run()
                )
