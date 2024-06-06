import logging
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, errors
from telethon.tl.types import MessageMediaPhoto
from utils.logging.logginconfig import setup_logger
from utils.db_connectors.firbase import FirebaseClient

# Load environment variables from a .env file
load_dotenv()

# Constants for Telegram API
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    print("Issue with keys: API_ID and/or API_HASH are not set properly.")
    exit(1)

# Set up logging
logger = setup_logger(__name__)

class TelegramUserClient:
    def __init__(self,session_name, api_id, api_hash):
        # Initialize the Telegram client
        self.client = TelegramClient(session_name, api_id, api_hash)
        
        
        
    async def start(self):
        # Start the Telegram client
        if not self.client.is_connected():
            await self.client.start()
            logger.info("Telegram client started.")
        else:
            logger.info("Telegram client already connected.")
    

    async def send_message(self, target_username, message):
        # Send a message to the specified chat or user
        if not self.client.is_connected():
            await self.client.start()
        

        MAX_MESSAGE_LENGTH = 4096
        message_parts = [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]
        

        try:
            entity = await self.client.get_entity(target_username)
            for msg in message_parts:
                await self.client.send_message(entity, msg)
                logger.info(f"Message sent to {target_username}: {message}")
        except errors.UsernameNotOccupiedError:
            logger.error(f"Username {target_username} is not occupied. Please check the username.")
        except Exception as e:
            logger.error(f"Failed to send message to {target_username}: {str(e)}")


    
    async def stop(self):
        # Stop the Telegram client
        if self.client.is_connected():
            await self.client.disconnect()
            logger.info("Telegram client stopped.")
        else:
            logger.info("Telegram client was not connected.")



    async def download_photo(self, media):
        file_path = await self.client.download_media(media)
        return file_path

   
   
    async def read_recent_messages(self,target_chat_username, limit=12):
        # Asynchronously read the last {limit} messages from the specified chat
        await self.start()
       
        messages_dict_list = []
        async for message in self.client.iter_messages(target_chat_username, limit=limit):
            logger.info(f"Message from {message.sender_id} content: {message.message}")
            message_dict = message.to_dict()
            message_dict['id'] = message.id 
            messages_dict_list.append(message_dict)
        
        # await self.client.run_until_disconnected()
        return  messages_dict_list   

    
      

