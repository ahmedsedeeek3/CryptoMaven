import os

from utils.logging.logginconfig import setup_logger
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

logging = setup_logger(__name__)

class OpenAIGen:
    def __init__(self,openai_clint,firbase_clint) -> None:
        self.openAi = openai_clint
        self.firebase_client_teleg = firbase_clint

        # self.openAi = OpenAIChat()
        # self.firebase_client_teleg = FirebaseClient(app_name="missionx", 
        #                                             collection_name="telegramMessages")
        
        '''
        respos:call db for (not AI) not yet reviesed and genrat differen
        messages for differen targets 
        '''
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

    def get_generate_teleg_savedb(self):
        self.openAi.set_system_message(self.sysROlPrombet.get("teleg"))
        docs = self.firebase_client_teleg.get_documents_where_ai_is_false()
        if len(docs)== 0 :
            logging.warning(msg="ERRO doc retrived with ai false len is 0")
            
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
                
                # [ai] TO [TRUE] indicating revised  
                ref = self.firebase_client_teleg.db.collection("telegramMessages").document(doc_id)
                ref.update({"ai": True})
                msgs += message
                
            except Exception as e:
                logging.error(f"Error processing document {doc.get('id', 'unknown')}: {e}")
        
        logging.info(f"Total messages: {msgs}")
        response = self.openAi.get_response(msgs)

        # Split message if it exceeds Telegram's character limit
        
        doc = {
            "ai_message": response[0],
            "used_token":response[1],
            "source": msgs,
            "sent": False
        }
        try:

            self.firebase_client_teleg.db.collection(self.collection_nameing.get("teleg", "")).add(doc)
            logging.info(f"doc add to db {doc}")
            
        except Exception as e:
           
            logging.info(f"error adding document to db {e}")

        
