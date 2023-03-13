from abc import ABC, abstractmethod
from typing import Coroutine

import asyncio
from fastapi import HTTPException

from conf import settings
from conf.settings import logger
from handlers.abstract import Handler
from util import messages


class CheckerError(Exception):
    pass


class Checker(ABC):
    """
    Base class for checkers. An instance represents a single server.
    Knows how to run, check and alert itself, start periodic monitoring.
    Subclasses must define abstract methods.
    """
    name = ''

    def __init__(
        self,
        host: str,
        port: int | None = None,
        handlers: list[Handler] = [],
        cycle: int | float | None = None,
        protocol: str = 'https',
        back_to_normal: bool = False,
        back_to_normal_cycle: int | float | None = None,
        include_normal: bool = False,   # Alert regardless of status,
        not_normal_for: int = 1
        ):
        self.host = host
        self.port = port
        self.handlers = handlers
        self.cycle = cycle
        self.protocol = protocol
        self.back_to_normal = back_to_normal
        self.back_to_normal_cycle = back_to_normal_cycle
        self.last_check = {}
        self.include_normal = include_normal

        self.not_normal_for = not_normal_for
        self._failed_count = 0          # not_normal_for count


    def __str__(self):
        return f'{self.__class__.__name__}({self.host})'

    @property
    def url(self):
        return f'{self.protocol}://{self.host}{self.port if self.port else ""}/'

    @property
    def _message_header(self):
        return f'Host: {self.host}\n'

    async def run(self):
        """Run a check, store results, alert if something is not normal."""
        self.result = await self.check()
        if self.result['status']:
            self._failed_count = 0
        else:
            self._failed_count += 1
            if self._failed_count >= self.not_normal_for:
                await self.alert(self.result)
                if self.back_to_normal:
                    await self.back_to_normal_monitor()

    async def check(self) -> dict:
        try:
            await self._get_data()
        except Exception as e:
            logger.debug(f"Couldn't check {self.name.capitalize()} on {self.host}: {e.__class__.__name__} {str(e)}")
            status = False
            message = messages.prepare_error_message(self, e)
        else:
            status = self._parse_data()
            message = self._prepare_message()
        return {
            'host': self.host,
            'check': self.name,
            'status': status,
            'message': message
        }

    @abstractmethod
    async def _get_data(self) -> None:
        """Request data from server, store in an attribute, return `None`"""
        ...

    @abstractmethod
    def _parse_data(self) -> bool:
        """Parse data, store results in an attribute, return server status (`bool`)"""
        ...

    @abstractmethod
    def _prepare_message(self) -> str:
        """Prepare a message based on parsed results, return `str`"""
        ...

    async def alert(self, result: dict):
        """Send message through handlers"""
        await asyncio.gather(*(handler.handle(result) for handler in self.handlers))

    async def monitor(self) -> Coroutine:
        if not self.handlers or not self.cycle:
            raise CheckerError(f'Trying to start {self} monitoring without handlers or cycle defined.')
        while True:
            logger.debug(f'Running {self}')
            try:
                await self.run()
            except:
                logger.exception(f'Exception during the monitoring {self}')
            else:
                logger.debug(f'Finished {self}')
            await asyncio.sleep(self.cycle)  # type: ignore

    async def back_to_normal_monitor(self) -> None:
        """Do follow up checks until `status` is `True`, send "back to normal" message"""
        if not self.back_to_normal_cycle:
            raise CheckerError(f'Trying to start {self} follow up monitoring without back_to_normal_cycle defined.')
        while True:
            await asyncio.sleep(self.back_to_normal_cycle)  # type: ignore
            logger.debug(f'Follow up {self}')
            try:
                followup_result = await self.check()
            except:
                logger.exception(f'Exception during follow up {self}')
            else:
                if followup_result['status']:
                    break
        logger.debug(f'Finished follow up {self}: back to normal')
        followup_result['message'] = f'{self} is back to normal'
        await self.alert(followup_result)

    @classmethod
    async def check_hosts(cls, hosts: list[str] | None = None) -> list[dict]:
        hosts_to_check = cls._parse_hosts(hosts)
        tasks = (cls(host=host, include_normal=True, **params).check() for host, params in hosts_to_check.items())
        return await asyncio.gather(*tasks)

    @classmethod
    def _parse_hosts(cls, hosts: list[str] | None = None) -> dict:
        """Verify that all hosts are defined in settings"""
        servers = settings.CHECKERS.get(cls.name, {}).get('servers')
        if not servers:
            raise HTTPException(500, f"{cls.name.capitalize()}Checker doesn't have any servers")

        if hosts:
            try:
                hosts_to_check = {host: servers[host] for host in hosts}
            except KeyError as e:
                raise HTTPException(400, f'Unknown host {e.args[0]}')
        else:
            hosts_to_check = servers

        return hosts_to_check

    @classmethod
    def extract_unknown_hosts(cls, hosts: list[str]) -> tuple[list[str], list[str]]:
        servers = settings.CHECKERS.get(cls.name, {}).get('servers', {})
        known_hosts = []
        unknown_hosts = []
        for host in hosts:
            if host in servers:
                known_hosts.append(host)
            else:
                unknown_hosts.append(host)
        return known_hosts, unknown_hosts
