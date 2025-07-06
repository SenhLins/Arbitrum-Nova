import asyncio
from loguru import logger
from classes.Account import Account
from config import TOKENS, WETH_ABI


class WrapETH(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain='arbitrum-nova')
        
        self.weth_address = self.w3.to_checksum_address(TOKENS['WETH'])
        self.weth_contract = self.get_contract(self.weth_address, WETH_ABI)
        
    async def wrap(self, min_amount: float, max_amount: float, decimal: int, unwrap: bool, unwrap_full_balance: bool):
        logger.info(f'{self.account_id} | {self.address} | Wrap ETH.')

        amount_wei, amount, balance = await self.get_amount(min_amount, max_amount, decimal, False, 5, 10)
        
        if amount_wei > balance:
            return logger.error(f'{self.account_id} | {self.address} | Insufficient funds for Wrap ETH.')

        tx_data = await self.get_tx_data(value=amount_wei)
    
        contract_txn = await self.weth_contract.functions.deposit().build_transaction(tx_data)
    
        signed_txn = await self.sign(contract_txn)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash)
        
        if unwrap:
            await self.unwrap(amount_wei, unwrap_full_balance)
        
    async def unwrap(self, amount_wei, unwrap_full_balance: bool):
        logger.info(f'{self.account_id} | {self.address} | Unwrap ETH.')
        
        balance = await self.get_balance(self.weth_address)
        balance_wei = balance['balance_wei']

        while amount_wei > balance_wei:
            asyncio.sleep(1)
            balance = await self.get_balance(self.weth_address)
            balance_wei = balance['balance_wei']
            
        if unwrap_full_balance: amount_wei = balance_wei

        tx_data = await self.get_tx_data()
    
        contract_txn = await self.weth_contract.functions.withdraw(amount_wei).build_transaction(tx_data)
    
        signed_txn = await self.sign(contract_txn)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash)