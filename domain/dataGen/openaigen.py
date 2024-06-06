import os
import asyncio
from utils.logging.logginconfig import setup_logger
from utils.db_connectors.firbase import FirebaseClient
from utils.ai_connectors.open_ai import OpenAIChat
from utils.social_conctors.telegramUser import TelegramUserListener
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

logging = setup_logger(__name__)

class OpenAIGen:
    def __init__(self) -> None:
        self.openAi = OpenAIChat()
        self.firebase_client_teleg = FirebaseClient(app_name="missionx", 
                                                    collection_name="telegramMessages")
        self.telegram = TelegramUserListener(session_name="reader",
                                             api_id=API_ID,
                                             api_hash=API_HASH,
                                             target_chat_username="@trending")

        self.collection_nameing = {
            "teleg": "teleg",
        }

        self.sysROlPrombet = {
            "teleg": '''
                    Read the following text and generate an engaging telegram listing the trending cryptocurrency coins must with
                    their ticker symbols, and price change. Use relevant emojis to make it attractive. No links or social media references.
                    End with a call to action to follow for hourly insights don't miss any coin.
                    Tweet Example:
                    🔥 <here add intro hot text>:
                    BTC $34.5k 🚀
                    ETH $2.6k 🌟
                    BNB $350 🔥
                    ADA $1.5 💎
                    SOL $40 🚀
                    ..... all coins don't miss any one
                    Follow us for hourly insights!
                    '''
        }

    async def get_generate_teleg_save_mesg(self):
        self.openAi.set_system_message(self.sysROlPrombet.get("teleg"))
        docs = self.firebase_client_teleg.get_documents_where_ai_is_false()
        msgs = ""
        last_doc_id = None

        for doc in docs:
            try:
                doc_id = doc["id"]
                last_doc_id = doc_id
                if not doc_id:
                    logging.error("Document does not contain an 'id' field")
                    continue

                message = doc.get('message', '')
                if not message:
                    continue
                
                ref = self.firebase_client_teleg.db.collection("telegramMessages").document(doc_id)
                ref.update({"ai": True})
                msgs += message
                
            except Exception as e:
                logging.error(f"Error processing document {doc.get('id', 'unknown')}: {e}")
        
        logging.info(f"Total messages: {msgs}")
        response = await self.openAi.get_response(msgs)

        # Split message if it exceeds Telegram's character limit
        MAX_MESSAGE_LENGTH = 4096
        response_parts = [response[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
        
        for part in response_parts:
            try:
                await self.telegram.send_message("@cryptoMissionX", part)
                logging.info(f"Message sent to @cryptoMissionX: {part}")
            except Exception as e:
                logging.error(f"Failed to send message to @cryptoMissionX: {e}")
        
        doc = {
            "ai_message": response,
            "source": msgs,
            "sent": False
        }
        self.firebase_client_teleg.db.collection(self.collection_nameing.get("teleg", "")).add(doc)
        if last_doc_id:
            logging.info(f"Updated document {last_doc_id} with AI response.")

async def main():
    generator = OpenAIGen()
    async with generator.telegram.client:
        await generator.get_generate_teleg_save_mesg()

if __name__ == "__main__":
    asyncio.run(main())
