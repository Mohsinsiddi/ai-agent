""" Cryptocurrency transaction handler implementation with Redis queue support. """
import json
from typing import List
from web3 import Web3
from redis.asyncio import Redis
from ..handlers.base import MessageHandler
from ..core.message import Message, MessageType
from ..utils.logger import logger
from ..config import ERC20_ABI, REDIS_URL

class CryptoTransferHandler(MessageHandler):
    def __init__(
        self,
        web3: Web3,
        token_address: str,
        source_address: str,
        target_address: str,
        private_key: str
    ):
        self.web3 = web3
        self.token_address = token_address
        self.source_address = source_address
        self.target_address = target_address
        self.private_key = private_key
        self.redis = None

    async def initialize(self):
        """Initialize Redis connection."""
        if not self.redis:
            self.redis = Redis.from_url(REDIS_URL, decode_responses=True)

    def supported_message_types(self) -> List[MessageType]:
        return [MessageType.TEXT]

    async def can_handle(self, message: Message) -> bool:
        return (
            isinstance(message.content, str) 
            and "crypto" in message.content.lower()
        )

    async def handle(self, message: Message, agent: 'AutonomousAgent') -> None:
        """Queue crypto transfer for background processing."""
        await self.initialize()

        transfer_data = {
            'token_address': self.token_address,
            'source_address': self.source_address,
            'target_address': self.target_address,
            'private_key': self.private_key,
            'amount': 1,  # Fixed amount for demo
            'web3_provider': self.web3.provider.endpoint_uri
        }

        await self.redis.lpush('crypto_transfers', json.dumps(transfer_data))
        logger.info(f"💸 Token transfer queued for processing")
        logger.info(f"   From: {self.source_address[:6]}...{self.source_address[-4:]}")
        logger.info(f"   To: {self.target_address[:6]}...{self.target_address[-4:]}")