import os
import time
import asyncio
from dotenv import load_dotenv
from utils.db_connectors.firbase import FirebaseClient
from utils.social_conctors.telegramUser import TelegramUserClient
from utils.ai_connectors.open_ai import OpenAIChat
from domain.dataGen.openaigen import OpenAIGen
from domain.dataCollecting.collect_data import CollectDataTodb
from domain.publishing.scheduled import SchaduledMessage
from utils.logging.logginconfig import setup_logger

#
load_dotenv()
logging = setup_logger(__name__)

# Constants for Telegram API
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
# x.com
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET_KEY")
bearer_token = os.environ.get("BEARER_TOKEN")

#  target_chat_username="@trending"

# clints init
telegram_client = TelegramUserClient(session_name="reader",
                                  api_id=API_ID,
                                  api_hash=API_HASH,
                                 )



firbase_clint = FirebaseClient(app_name="missionx",collection_name="telegramMessages")
open_ai_chat_client = OpenAIChat()

# domain clint 
schaduledMessage = SchaduledMessage(telegram_client = telegram_client ,firbase_client = firbase_clint)
collectDataTodb = CollectDataTodb(firbase_client=firbase_clint,telegram_clint=telegram_client)
openAiGenerator = OpenAIGen(openai_clint=open_ai_chat_client,firbase_clint=firbase_clint)

# 1-get messages fom telgram ----> the generat over it 

# operations :




#testing 


async def collect_telegram_data():
    try:
        logging.info("Starting to collect Telegram data...")
        await collectDataTodb.collect_telegram_byChanel_to_db(target_chat_username="@trending")
        logging.info("Finished collecting Telegram data.")
        await asyncio.sleep(30)
    except Exception as e:
        logging.error(f"Error in collect_telegram_byChanel_to_db: {e}")

def generate_telegram_data():
    try:
        logging.info("Starting to generate Telegram data...")
        openAiGenerator.get_generate_teleg_savedb()
        
    except Exception as e:
        logging.error(f"Error in get_generate_teleg_savedb: {e}")

async def send_telegram_messages():
    try:
        logging.info("Starting to send Telegram messages from DB...")
        await schaduledMessage.send_teleg_mesg_from_db()
        logging.info("Finished sending Telegram messages from DB.")
        await asyncio.sleep(30)
    except Exception as e:
        logging.error(f"Error in send_teleg_mesg_from_db: {e}")

async def main_loop():
    while True:
        await collect_telegram_data()
        generate_telegram_data()  # No await needed
        await asyncio.sleep(10)  # Added a short delay between tasks to ensure smooth execution
        await send_telegram_messages()

if __name__ == "__main__":
    asyncio.run(main_loop())