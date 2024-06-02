import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from utils.logging.logginconfig import setup_logger
# Load environment variables from a .env file
load_dotenv()

# Constants for Telegram API
API_ID = int(os.getenv("AP_id"))
API_HASH = os.getenv("App_api_hash")

if not API_ID or not API_HASH:
    print("Issue with keys: API_ID and/or API_HASH are not set properly.")
    exit(1)

# Set up logging
logger = setup_logger(__name__)

# Initialize user account to listen to various bots or chats
class TelegramUserListener:
    def __init__(self, session_name, api_id, api_hash, target_bot_username):
        # Initialize the Telegram client
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.target_bot_username = target_bot_username

    async def start(self):
        # Start the Telegram client
        await self.client.start()
        logger.info("Telegram client started.")
        
        


        # Add an event handler for new messages
        # self.client.add_event_handler(self.message_handler_async, events.NewMessage)
        # logger.info("Event handler added.")

        # Read the last 12 messages from a specific chat
        await self.read_messages_patches(limit=12)

    async def read_messages_patches(self, limit=12):
        # Asynchronously read the last {limit} messages from the specified chat
        message_list = []
        async for message in self.client.iter_messages(self.target_bot_username, limit=limit):
            logger.info(f"Message from {message.sender_id}:{message}")
            message_list.append(message)
        
        return message_list   
        
    
    #conect db and save messages for further action 
        #########
        ##missed block
        #########
            



    async def message_handler_async(self, event):
        # Receive new messages from a specific bot username in real-time
        if event.message.sender_id == self.target_bot_username:
            logger.info(f"Message from {self.target_bot_username}: {event.message.text}")

    def run(self):
        # Run the main function with the client
        with self.client:
            logger.info("Running the Telegram client.")
            self.client.loop.run_until_complete(self.start())

TeleClient = TelegramUserListener(session_name="reader",
                                  api_id=API_ID,
                                  api_hash=API_HASH,
                                  target_bot_username="@trending")

TeleClient.run()


class SendMessage:
    def __init__(self, session_name, api_id, api_hash):
        # Initialize the Telegram client
        self.client = TelegramClient(session_name, api_id, api_hash)

    async def start(self):
        # Start the Telegram client
        await self.client.start()
        logger.info("Telegram client started.")

    async def send_message(self, target_username, message):
        # Send a message to the specified username
        await self.client.send_message(target_username, message)
        logger.info(f"Sent message to {target_username}: {message}")

    def run(self, target_username, message):
        # Run the main function with the client
        with self.client:
            logger.info("Running the Telegram client.")
            self.client.loop.run_until_complete(self._run(target_username, message))

    async def _run(self, target_username, message):
        # Start the client and send the message
        await self.start()
        await self.send_message(target_username, message)