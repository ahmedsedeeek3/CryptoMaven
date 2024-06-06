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
load_dotenv()

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

async def main ():
    while True:
        await collectDataTodb.collect_telegram_byChanel_to_db(target_chat_username="@trending")
        newMessage = openAiGenerator.get_generate_teleg_savedb() 
        if newMessage :
        #  if new message is retrived the newly genrated message  
         await schaduledMessage.send_teleg_mesg_from_db()
        time.sleep(120)
asyncio.run(main())   