from loguru import logger
import time

from classes.Account import Account
from config import ARBSWAP_ABI_V1, ARBSWAP_ABI_V2, TOKENS, ARBSWAP_CONTRACT, ARBSWAP_CONTRACT_V2
from settings import SLIPPAGE


class ArbSwap(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain='arbitrum-nova')
        
        self.arbswap_contract = self.get_contract(ARBSWAP_CONTRACT, ARBSWAP_ABI_V1)
        self.arbswap_contract_v2 = self.get_contract(ARBSWAP_CONTRACT_V2, ARBSWAP_ABI_V2)

    async def swap(self, from_token: str, to_token: str, min_amount: float, max_amount: float, decimal: int, reverse_swap: bool):
        logger.info(f'{self.account_id} | {self.address} | {from_token} -> {to_token} | Swap on Arbswap.')

        from_token_address = self.w3.to_checksum_address(TOKENS[from_token])
        to_token_address = self.w3.to_checksum_address(TOKENS[to_token])

        amount_wei, amount, balance = await self.get_amount(from_token, min_amount, max_amount, decimal, False, 5, 10)
        
        tx_data = await self.get_tx_data()
        
        if amount_wei > balance:
            return logger.error(
                f'{self.account_id} | {self.address} | {from_token} -> {to_token} | Insufficient funds for Arbswap.'
            )

        if from_token == 'ETH':
            tx_data.update({'value': amount_wei})
        else:
            await self.approve(amount_wei, TOKENS[from_token], ARBSWAP_CONTRACT_V2)

        min_return = await self.get_amount_out(amount_wei, from_token, to_token)

        contract_txn = await self.arbswap_contract_v2.functions.swap(
            from_token_address,
            to_token_address,
            amount_wei,
            min_return,
            1
        ).build_transaction(tx_data)

        signed_txn = await self.sign(contract_txn)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash)
        
        if reverse_swap:
            return await self.swap(to_token, from_token, min_amount, max_amount, decimal, False)
        
    async def get_amount_out(self, amount_wei: int, from_token: str, to_token: str) -> int:
        if from_token == 'ETH': from_token = self.w3.to_checksum_address(TOKENS['WETH'])
        else: from_token = self.w3.to_checksum_address(TOKENS[from_token])

        if to_token == 'ETH': to_token = self.w3.to_checksum_address(TOKENS['WETH'])
        else: to_token = self.w3.to_checksum_address(TOKENS[to_token])
        
        amount_out = (await self.arbswap_contract.functions.getAmountsOut(amount_wei, [from_token, to_token]).call())[1]
        
        min_return = int(amount_out - (amount_out * SLIPPAGE // 100))

        return min_return

    async def add_liqudity(self, min_percent: int, max_percent: int):
        logger.info(f'{self.account_id} | {self.address} | Add liquidity on Arbswap.')
        
        usdc_address = self.w3.to_checksum_address(TOKENS['USDC'])
        
        amount_wei_usdc, amount_usdc, balance_usdc = await self.get_amount('USDC', 0.001, 0.001, 6, True, min_percent, max_percent)
        amount_wei_eth = await self.get_amount_out(amount_wei_usdc, 'USDC', 'ETH')
        
        amount_min_usdc = int(amount_wei_usdc - (amount_wei_usdc * SLIPPAGE // 100))
        amount_min_eth = int(amount_wei_eth - (amount_wei_eth * SLIPPAGE // 100))
        
        await self.approve(amount_wei_usdc, usdc_address, ARBSWAP_CONTRACT)
        
        tx_data = await self.get_tx_data(value=amount_wei_eth)
        
        deadline = int(time.time() + 10000)
        
        contract_txn = await self.arbswap_contract.functions.addLiquidityETH(
            usdc_address,
            amount_wei_usdc,
            amount_min_usdc,
            amount_min_eth,
            self.address,
            deadline
        ).build_transaction(tx_data)

        signed_txn = await self.sign(contract_txn)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash)