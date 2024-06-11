import time
from model.ai_questions import Ai_questions
from model.collections  import collectionNameing
from utils.logging.logginconfig import setup_logger


logger = setup_logger(__name__)

class CollectDataTokenmetrics:
    def __init__(self,tokenmetrics_conector,db_connector) -> None:
        self.tokenmetrics_conector = tokenmetrics_conector
        self.ai_questions = Ai_questions()
        self.collection_names = collectionNameing()
        self.db  = db_connector

    
    def genrat_day_questions_res_tokenAi(self):
        questions = self.ai_questions.day_questions()
        c = "Which altcoins are trending right now?"
        for k,q in questions.items():
            try:
                time.sleep(35)
                state , answer = self.tokenmetrics_conector.token_metrics_chat_bot(c)
                if  state is None:
                    logger.warning(f"genrat_day_questions_res stat -->{state}")
                    continue
                logger.info(f"genrat_day_questions_res-->stat{k} answer {answer}")
                
                data = {
                   "time_to_send":time.time(),
                   "question":q,
                   "answer":answer,
                   "ai":False
                } 
                self.db.add_document(self.collection_names.collection_name()["daily_q"],data)
            except Exception as e:
                logger.warning(f"{e}")



    def get_sementem_to_db(self):
        try: 
            state , answer = self.tokenmetrics_conector.get_sentiments()
            if  state is None:
                        logger.warning(f"conector.get_sentiments stat -->{state}")
                        return
            data = {
                    "time":time.time(),
                    "question":"sementem",
                    "answer":answer,
                    "ai":False,
                    } 
            self.db.add_document(self.collection_names.collection_name()["sementem"],data)
        except Exception as e:
                logger.warning(f"{e}")