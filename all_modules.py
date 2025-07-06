import random

from modules.arbswap import ArbSwap
from modules.wrapeth import WrapETH


async def random_route(account_id: int, key: str, proxy: str):
    
    # Insert the functions below that you want to use for random selection
    all_modules = [
        arbswap_swap,
        arbswap_add_liqudity,
        wrap_eth
    ]
    
    choice = random.choice(all_modules)
    await choice(account_id, key, proxy)

async def arbswap_swap(account_id: int, key: str, proxy: str):
    from_token = 'ETH'
    to_token = 'USDC'
    
    reverse_swap = True
    
    min_amount = 0.000045
    max_amount = 0.000065
    decimal = 6
    
    arbswap = ArbSwap(account_id, key, proxy)
    await arbswap.swap(from_token, to_token, min_amount, max_amount, decimal, reverse_swap)

async def arbswap_add_liqudity(account_id: int, key: str, proxy: str):
    min_percent = 100
    max_percent = 100
    
    arbswap = ArbSwap(account_id, key, proxy)
    await arbswap.add_liqudity(min_percent, max_percent)
    
async def wrap_eth(account_id: int, key: str, proxy: str):
    min_amount = 0.000045
    max_amount = 0.000065
    decimal = 6

    unwrap_eth = True
    unwrap_full_balance = True

    wrap_eth = WrapETH(account_id, key, proxy)
    await wrap_eth.wrap(min_amount, max_amount, decimal, unwrap_eth, unwrap_full_balance)