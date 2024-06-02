import os
import pytest
from unittest.mock import AsyncMock, patch
from utils.social_conctors.telegramUser import TelegramUserListener
from utils.logging.logging_config import setup_logger

# Mock environment variables
@patch.dict(os.environ, {'AP_id': '123456', 'App_api_hash': 'fake_api_hash'})
def test_initialization():
    listener = TelegramUserListener('test_session', 123456, 'fake_api_hash', '@test_bot')
    assert listener.client is not None
    assert listener.target_bot_username == '@test_bot'

# Test the start method
@pytest.mark.asyncio
@patch('social_conctors.telgram.TelegramClient')
async def test_start(mock_telegram_client):
    mock_client_instance = mock_telegram_client.return_value
    mock_client_instance.start = AsyncMock()
    mock_client_instance.iter_messages = AsyncMock(return_value=[])
    
    listener = TelegramUserListener('test_session', 123456, 'fake_api_hash', '@test_bot')
    
    await listener.start()
    
    mock_client_instance.start.assert_awaited_once()
    mock_client_instance.add_event_handler.assert_called_once()

# Test read_messages_patches method
@pytest.mark.asyncio
@patch('social_conctors.telgram.TelegramClient')
async def test_read_messages_patches(mock_telegram_client):
    mock_client_instance = mock_telegram_client.return_value
    mock_client_instance.iter_messages = AsyncMock(return_value=[
        AsyncMock(sender_id='123', text='Test message 1'),
        AsyncMock(sender_id='456', text='Test message 2')
    ])
    
    listener = TelegramUserListener('test_session', 123456, 'fake_api_hash', '@test_bot')
    
    await listener.read_messages_patches(limit=2)
    
    mock_client_instance.iter_messages.assert_awaited_once_with('@test_bot', limit=2)

# Test message_handler_async method
@pytest.mark.asyncio
@patch('social_conctors.telgram.TelegramClient')
async def test_message_handler_async(mock_telegram_client):
    mock_client_instance = mock_telegram_client.return_value
    mock_event = AsyncMock()
    mock_event.message.sender_id = '@test_bot'
    mock_event.message.text = 'Test message'
    
    listener = TelegramUserListener('test_session', 123456, 'fake_api_hash', '@test_bot')
    
    await listener.message_handler_async(mock_event)
    
    assert listener.target_bot_username == '@test_bot'
