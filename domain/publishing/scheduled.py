from utils.logging.logginconfig import setup_logger

logger = setup_logger(__name__)

class SchaduledMessage:
    def __init__(self,telegram_client,firbase_client) -> None:
        self.telegram_client = telegram_client
        self.firbase_client  = firbase_client

    
    async def send_teleg_mesg_from_db(self):
        try:
         mesgs = self.firbase_client.get_documents_where_sent_is_false_telg()
        except Exception as e :
         logger.error(f"Error : get_documents_where_sent_is_false_telg {e} ")
        if len(mesgs) == 0 : 
                logger.error(f"Error : get_documents_where_sent_is_false_telg return 0 ")
                return
        for mesg in mesgs:
                logger.info(f"message id : {mesg}")
                await self.telegram_client.send_message(target_username="@cryptoMissionX",message = mesg['ai_message'])
 
           

           

     