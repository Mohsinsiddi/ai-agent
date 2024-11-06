"""
Cryptocurrency transaction handler implementation.

This module provides a handler that processes crypto-related messages
and executes token transfers.
"""

import json
from typing import List
from web3 import Web3
from eth_account import Account
from ..handlers.base import MessageHandler
from ..core.message import Message, MessageType
from ..utils.logger import logger
from ..config import ERC20_ABI

class CryptoTransferHandler(MessageHandler):
    """Handler for processing cryptocurrency transfers."""
    
    def __init__(
        self,
        web3: Web3,
        token_address: str,
        source_address: str,
        target_address: str,
        private_key: str
    ):
        """
        Initialize the handler.
        
        Args:
            web3 (Web3): Web3 instance
            token_address (str): Token contract address
            source_address (str): Source wallet address
            target_address (str): Target wallet address
            private_key (str): Private key for source wallet
        """
        self.web3 = web3
        self.token_contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(token_address),
            abi=json.loads(ERC20_ABI)
        )
        self.source_address = self.web3.to_checksum_address(source_address)
        self.target_address = self.web3.to_checksum_address(target_address)
        self.private_key = private_key
        self.account = Account.from_key(private_key)

    def supported_message_types(self) -> List[MessageType]:
        """
        Get supported message types.
        
        Returns:
            List[MessageType]: List containing TEXT message type
        """
        return [MessageType.TEXT]

    async def can_handle(self, message: Message) -> bool:
        """
        Check if message contains "crypto".
        
        Args:
            message (Message): Message to check

        Returns:
            bool: True if message contains "crypto", False otherwise
        """
        return (
            isinstance(message.content, str) and
            "crypto" in message.content.lower()
        )

    async def handle(self, message: Message, agent: 'AutonomousAgent') -> None:
        """
        Process crypto transfer message.
        
        Args:
            message (Message): Message to process
            agent (AutonomousAgent): Agent processing the message
        """
        try:
            # Check balance
            balance = self.token_contract.functions.balanceOf(self.source_address).call()
            logger.info(f"💰 Current balance before transfer: {balance}")
            
            if balance >= 1:
                # Get nonce
                nonce = self.web3.eth.get_transaction_count(self.source_address)
                
                # Create transfer function
                transfer_function = self.token_contract.functions.transfer(
                    self.target_address,
                    1  # Transfer 1 token unit
                )
                
                # Build transaction
                # Get base fee
                base_fee = self.web3.eth.get_block('latest').baseFeePerGas

                # Calculate max priority fee (tip)
                max_priority_fee = self.web3.eth.max_priority_fee

                # Calculate max fee (base fee + priority fee + buffer)
                max_fee_per_gas = (2 * base_fee) + max_priority_fee

                # # Build transaction with EIP-1559 parameters
                # txn = transfer_function.build_transaction({
                #     'from': self.source_address,
                #     'nonce': nonce,
                #     'gas': 1000000,
                #     'maxFeePerGas': max_fee_per_gas,
                #     'maxPriorityFeePerGas': max_priority_fee,
                #     'chainId': self.web3.eth.chain_id,
                #     'type': 2  # EIP-1559 transaction type
                # })
                
                # Build transaction with higher gas price
                txn = transfer_function.build_transaction({
                    'from': self.source_address,
                    'nonce': nonce,
                    'gas': 1000000,
                    'gasPrice': int(self.web3.eth.gas_price * 10),  # Increase gas price by 20%
                    'chainId': self.web3.eth.chain_id
                })
                # Sign transaction
                signed_txn = Account.sign_transaction(txn, self.private_key)
                
                # Send transaction
                tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                
                logger.info(f"💸 Token transfer initiated")
                logger.info(f"📝 Transaction details:")
                logger.info(f"   From: {self.source_address[:6]}...{self.source_address[-4:]}")
                logger.info(f"   To: {self.target_address[:6]}...{self.target_address[-4:]}")
                logger.info(f"   Amount: 1 token")
                logger.info(f"   Transaction Hash: {tx_hash.hex()}")
                
                # Wait for transaction receipt
                receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
                if receipt['status'] == 1:
                    logger.info(f"✅ Transaction confirmed! Gas used: {receipt['gasUsed']}")
                else:
                    logger.error(f"❌ Transaction failed!")
                
            else:
                logger.warning(f"⚠️ Insufficient balance in source wallet: {balance}")
                
        except Exception as e:
            logger.error(f"❌ Failed to transfer token: {str(e)}")
            logger.error(f"   Source: {self.source_address}")
            logger.error(f"   Target: {self.target_address}")