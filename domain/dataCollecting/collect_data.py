import os
from dotenv import load_dotenv 
from utils.social_conctors.telegramUser import  TelegramUserListener
load_dotenv()








class collectDataTodb:
    def __init__(self) -> None:
        self.api_id = int(os.getenv("API_ID"))
        self.api_hash =  os.getenv("API_HASH")
        

     
    async def collect_telegram(self,channel_id):
        self.TelegramUserListener =  TelegramUserListener(session_name="reader",
                                  api_id=self.api_id,
                                  api_hash=self.api_hash,
                                  target_chat_username=channel_id)
        
        await self.TelegramUserListener.run()

    
    
    
   