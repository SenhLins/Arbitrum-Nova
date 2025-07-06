from concurrent.futures import ThreadPoolExecutor
import random
import reade
import sys
import time
from typing import Callable
from loguru import logger
import questionary
from questionary import Choice

from settings import DEBUG_MODE, QUANTITY_THREADS, RANDOM_WALLET, THREAD_SLEEP_FROM, THREAD_SLEEP_TO
from all_modules import *
from utils.utils import _async_run_module, get_wallets, get_wallet_address


def get_module():
    result = questionary.select(
        'Select a method to get started',
        choices=[
            Choice('1) Random Module', random_route),
            Choice('2) ARBSwap Swap', arbswap_swap),
            Choice('3) ARBSwap Add Liqudity', arbswap_add_liqudity),
            Choice('4) Wrap ETH', wrap_eth),
            Choice('5) Exit', 'exit')
        ],
        qmark='⚙️ ',
        pointer='✅ '
    ).ask()
    
    if result == 'exit':
        sys.exit()
    return result

def main(module: Callable):
    wallets = get_wallets()
    
    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            future = executor.submit(
                _async_run_module,
                module,
                account.get('id'),
                account.get('key'),
                account.get('proxy')
            )
            if DEBUG_MODE:
                exception = future.exception()
                exception_msg = (f'{account.get("id")} | {get_wallet_address(account.get("key"))} | {exception}')
                logger.error(exception_msg) if exception else time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))
            else:
                time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))
    
if __name__ == '__main__':
    logger.add('logging.log')
    module = get_module()
    main(module)