from fastapi import APIRouter

import checkers


router = APIRouter(prefix='/check')


@router.post('/all/')
async def full_check():
    #TODO: optionally run in the background
    await checkers.full_check()

@router.get('/queues/')
async def queues(hosts: list[str] | None = None) -> list[dict]:
    """Current queues size"""
    return await checkers.FlowerChecker.check_hosts(hosts)

@router.get('/ping/')
async def ping(hosts: list[str] | None = None) -> list[dict]:
    """Current queues size"""
    return await checkers.PingChecker.check_hosts(hosts)
