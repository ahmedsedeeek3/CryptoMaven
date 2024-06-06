import asyncio
from utils.db_connectors.firbase import FirebaseClient
import time 
from utils.social_conctors.telegramUser import TelegramUserListener
from dotenv import load_dotenv
import os
from utils.social_conctors.twitter import TwitterOAuth
from utils.ai_connectors.open_ai import OpenAIChat
from domain.dataGen.openaigen import OpenAIGen
from domain.dataCollecting.collect_data import collectDataTodb
load_dotenv()

# Constants for Telegram API
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
# x.com
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET_KEY")
bearer_token = os.environ.get("BEARER_TOKEN")
collectDataTodb =collectDataTodb()
generator = OpenAIGen()
# https://t.me/+w89MI4kxRqRmZjZk

TeleClient = TelegramUserListener(session_name="reader",
                                  api_id=API_ID,
                                  api_hash=API_HASH,
                                  target_chat_username="@trending")

TeleClient.run()


    # TeleClient.send_message("+w89MI4kxRqRmZjZk","any")
# asyncio.run(TeleClient.send_message("@cryptoMissionX", "This is a test message!"))

# async def send_message():
#     await TeleClient.send_message("@cryptoMissionX", "This is a test10 message!")    
# asyncio.run(send_message())
# TeleClient.run()
# Twitter = TwitterOAuth(consumer_key, consumer_secret,bearer_token)




# payload = {"text": '''one more time  Crypto Market Update: June 4, 2024 🌐💹
# Fear & Greed Index: Greed (73) 🟢
# Market Cap: $2.56T (+0.01%) 📈
# BTC: $68.9K (+0.31%) 🟩
# ETH: $3.76K (-1.35%) 🟥
# BTC Dominance: 54.59% 🔥
# '''}
# "go_publish":True,
#                     "ai":False,
#                     "ai_teleg_completed":False,
#                     "ai_twitter_completed":False,
#                     "ai_twitch_completed":False,
#                     "ai_telegram_marketing_completed":False,
#                     "ai_teleg_completed":False,
#                     "ai_message_telegram_bot":"",
#                     "ai_message_twitter":"",
#                     "ai_message_twitch":"",
#                     "ai_message_telegram_marketing":"",
#                     "img":img,
#                     "img_url":photo_path,
#                     "published_tel":False,
#                     "published_twitter":False,
#                     "published_twitch":False,
#                     "published_marketing":False,


# Set a document
    

# openai_chat = OpenAIChat()

async def fun():
    await collectDataTodb.collect_telegram("@trending")
    await generator.telegram.client.start()
    await generator.get_generate_teleg_save_mesg()
    await generator.telegram.client.disconnect()




while  True :
#     # Twitter.sendMessage(payload=payload)
#     # TeleClient.run()
#     # Twitter.listen_to_tweets()
#     # for i in range(100):
#     #   firestore_client.set_document(f"alovelace+{i}", {"first": "Ada", "last": "Lovelace", "born": 1815})
      

    asyncio.run(fun())
    time.sleep(200)
#     # openai_chat.set_system_message("You are a helpful assistant.")
    # response, tokens_used = openai_chat.get_response("Hello, how are you?")
    # print("Response:", response)
    # print("Tokens used:", tokens_used)

  
    # Get a document
    # doc_data = firestore_client.get_document("alovelace")
    
    # Update a document
    # firestore_client.update_document("alovelace", {"last": "Byron"})
    # print(doc_data)
    # Delete a document
    # firestore_client.delete_document("alovelace")
    
  
