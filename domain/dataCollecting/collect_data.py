from utils.logging.logginconfig import setup_logger


logger = setup_logger(__name__)
class CollectDataTodb:
    def __init__(self,telegram_clint,firbase_client) -> None:
        self.telegram_clint = telegram_clint
        self.firbase_client = firbase_client
        
        

     
    async def collect_telegram_byChanel_to_db(self,target_chat_username):
        try:  
            messages_dict_list = await self.telegram_clint.read_recent_messages(target_chat_username)
            
            for msg in  messages_dict_list:
                self.firbase_client.save_message_to_firestore(msg)
 
        except Exception as e:
            logger.error(f"Failed to recive message  {e}")
         
          
        

        
        
            

    
    
    
   