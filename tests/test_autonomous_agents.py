from autonomous_agents.behaviors.random_message import RandomMessageBehavior
from autonomous_agents.core.agent import AutonomousAgent
from autonomous_agents.core.message import Message, MessageType
from autonomous_agents.handlers.crypto import CryptoTransferHandler
from autonomous_agents.handlers.hello import HelloMessageHandler
import pytest
import asyncio
from unittest.mock import Mock, patch
from web3 import Web3
from eth_account import Account
from datetime import datetime


# Test Configuration
TEST_TOKEN_ADDRESS = "0x77f565d1f11ad8ecff3e55cf1cde77bb6b189e44"
TEST_WALLET1_ADDRESS = "0x5d1d0b1d5790b1c88cc1e94366d3b242991dc05d"
TEST_WALLET2_ADDRESS = "0x5d1d0b1d5790b1c88cc1e94366d3b242991dc05d"
TEST_TARGET_ADDRESS = "0xabAB8096c7C9922F991772164311Ba862bCE7622"
TEST_PRIVATE_KEY = "d15c43126f6966491820b8dc093a3ebed8ff48fa980ce52105f34d2296b228dc"

# Fixtures
@pytest.fixture
def web3_mock():
    with patch('web3.Web3') as mock:
        # Mock essential Web3 methods
        mock.to_checksum_address = lambda x: x
        mock.eth.chain_id = 1
        mock.eth.gas_price = 20000000000
        mock.eth.get_transaction_count.return_value = 1
        
        # Mock contract interactions
        contract_mock = Mock()
        contract_mock.functions.balanceOf.return_value.call.return_value = 1000
        contract_mock.functions.transfer.return_value.build_transaction.return_value = {
            'to': TEST_TARGET_ADDRESS,
            'value': 0,
            'gas': 100000,
            'gasPrice': 20000000000,
            'nonce': 1,
            'chainId': 1
        }
        mock.eth.contract.return_value = contract_mock
        
        yield mock

@pytest.fixture
def agent():
    return AutonomousAgent("TestAgent")

# Unit Tests
@pytest.mark.asyncio
async def test_random_message_behavior():
    """Unit test for RandomMessageBehavior"""
    behavior = RandomMessageBehavior(interval=0)
    agent = AutonomousAgent("TestAgent")
    
    # Test should_act
    should_act = await behavior.should_act()
    assert should_act is True
    
    # Test act
    await behavior.act(agent)
    message = await agent.outbox.get()
    assert message is not None
    assert message.type == MessageType.TEXT
    assert isinstance(message.content, str)
    assert len(message.content.split()) == 2

@pytest.mark.asyncio
async def test_hello_message_handler():
    """Unit test for HelloMessageHandler"""
    handler = HelloMessageHandler()
    agent = AutonomousAgent("TestAgent")
    
    # Test with "hello" message
    hello_message = Message(
        type=MessageType.TEXT,
        content="hello world"
    )
    can_handle = await handler.can_handle(hello_message)
    assert can_handle is True
    
    # Test with non-hello message
    other_message = Message(
        type=MessageType.TEXT,
        content="test message"
    )
    can_handle = await handler.can_handle(other_message)
    assert can_handle is False

@pytest.mark.asyncio
async def test_crypto_transfer_handler(web3_mock):
    """Unit test for CryptoTransferHandler"""
    handler = CryptoTransferHandler(
        web3_mock,
        TEST_TOKEN_ADDRESS,
        TEST_WALLET1_ADDRESS,
        TEST_TARGET_ADDRESS,
        TEST_PRIVATE_KEY
    )
    agent = AutonomousAgent("TestAgent")
    
    # Test with crypto message
    crypto_message = Message(
        type=MessageType.TEXT,
        content="send some crypto"
    )
    can_handle = await handler.can_handle(crypto_message)
    assert can_handle is True
    
    # Test transaction handling
    with patch('eth_account.Account.sign_transaction') as mock_sign:
        mock_sign.return_value.rawTransaction = b'raw_transaction'
        web3_mock.eth.send_raw_transaction.return_value = b'tx_hash'
        web3_mock.eth.wait_for_transaction_receipt.return_value = {'status': 1, 'gasUsed': 100000}
        
        await handler.handle(crypto_message, agent)
        
        # Verify transaction was attempted
        assert web3_mock.eth.send_raw_transaction.called
        assert web3_mock.eth.wait_for_transaction_receipt.called

def test_agent_initialization():
    """Test agent initialization and configuration"""
    agent = AutonomousAgent("TestAgent")
    
    assert agent.name == "TestAgent"
    assert agent.inbox is not None
    assert agent.outbox is not None
    assert agent.handler_registry is not None
    assert agent.behavior_registry is not None
    assert not agent.running

# Run tests with: pytest test_autonomous_agents.py -v