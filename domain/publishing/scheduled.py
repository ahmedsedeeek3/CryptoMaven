from utils.logging.logginconfig import setup_logger

logger = setup_logger(__name__)

class SchaduledMessage:
    def __init__(self,telegram_client,firbase_client) -> None:
        self.telegram_client = telegram_client
        self.firbase_client  = firbase_client
    
    
    # crate scudel for messages 
        #respect roles 
        '''
        {target:{name:telegram,time:{
        "10:20":[id,id],
        "11:10":[id,id]

        }}}
        '''
    
    
    
    
    
    
    
    
    
    


    
    async def schaduled_message_from_db(self):
        '''
        check mssags in db then check schudel and 
        add them to schudel 
        '''
        try:
         mesgs = self.firbase_client.get_documents_where_sent_is_false_telg()
        
        except Exception as e :
         logger.error(f"Error : get_documents_where_sent_is_false_telg {e} ")
        if len(mesgs) == 0 : 
                logger.error(f"Error : get_documents_where_sent_is_false_telg return 0 ")
                return
        
        
        async for mesg in self.async_iterable(mesgs):
                logger.info(f"message id :")
                # check the scudel 
                # add message Id to is patfor acourding to scudel 
                
                await self.telegram_client.send_messages(target_username="@cryptoMissionX",message = mesg['ai_message'])
 
    








    # should be shifted to other place
    async def async_iterable(self,my_list):
        for item in my_list:
            yield item


    async def send_teleg_mesg_from_db(self):
        try:
         mesgs = self.firbase_client.get_documents_where_sent_is_false_telg()
        
        except Exception as e :
         logger.error(f"Error : get_documents_where_sent_is_false_telg {e} ")
        if len(mesgs) == 0 : 
                logger.error(f"Error : get_documents_where_sent_is_false_telg return 0 ")
                return
        async for mesg in self.async_iterable(mesgs):
                logger.info(f"message id :")
                await self.telegram_client.send_messages(target_username="@cryptoMissionX",message = mesg['ai_message'])
 
           

           

     