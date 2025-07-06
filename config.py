import json

with open('data/rpc.json', 'r') as file:
    RPC = json.load(file)
    
with open('data/erc20_abi.json', 'r') as file:
    ERC20_ABI = json.load(file)

with open('data/arbswap/abi_router_v1.json', 'r') as file:
    ARBSWAP_ABI_V1 = json.load(file)
    
with open('data/arbswap/abi_router_v2.json', 'r') as file:
    ARBSWAP_ABI_V2 = json.load(file)
    
with open('data/weth/abi.json', 'r') as file:
    WETH_ABI = json.load(file)

with open('accounts.txt', 'r') as file:
    ACCOUNTS = [row.strip() for row in file]
    
with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

ARBSWAP_CONTRACT = '0xEe01c0CD76354C383B8c7B4e65EA88D00B06f36f'
ARBSWAP_CONTRACT_V2 = '0x67844f0f0dd3D770ff29B0ACE50E35a853e4655E'

TOKENS = {
    'ETH': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
    'WETH': '0x722E8BdD2ce80A4422E880164f2079488e115365',
    'USDC': '0x750ba8b76187092B0D1E87E28daaf484d1b5273b',
    'ARB': '0xf823C3cD3CeBE0a1fA952ba88Dc9EEf8e0Bf46AD',
    'DAI': '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1'
}