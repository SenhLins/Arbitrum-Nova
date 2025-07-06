import asyncio
import random
from loguru import logger
from typing import Callable
from eth_account import Account as EthereumAccount

from config import ACCOUNTS, PROXIES
from settings import SLEEP_FROM, SLEEP_TO, USE_PROXY
from all_modules import *


async def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    
    logger.info(f'💤 Sleep {delay} s.')
    for _ in range(delay):
        await asyncio.sleep(1)

async def run_module(module: Callable, account_id: int, key: str, proxy: str):
    await module(account_id, key, proxy)

    await sleep(SLEEP_FROM, SLEEP_TO)

def _async_run_module(module: Callable, account_id: int, key: str, proxy: str):
    asyncio.run(run_module(module, account_id, key, proxy))
    
def get_wallets():
    if USE_PROXY:
        account_with_proxy = dict(zip(ACCOUNTS, PROXIES))
        
        wallets = [
            {
                'id': _id,
                'key': key,
                'proxy': account_with_proxy[key]
            } for _id, key in enumerate(account_with_proxy, start=1)
        ]
    else:
        wallets = [
            {
                'id': _id,
                'key': key,
                'proxy': None
            } for _id, key in enumerate(ACCOUNTS, start=1)
        ]
    return wallets

def get_wallet_address(key: str) -> str:
    account = EthereumAccount.from_key(key)
    return account.address