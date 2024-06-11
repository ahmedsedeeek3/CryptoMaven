from model import open_ai_prompets
from model import collections
from utils.logging.logginconfig import setup_logger
collections_names = collections().collction_name()


logger = setup_logger(__name__)





class PubToTwitterFromDb:
    
    def __init__(self,dbClint,openAiClint) -> None:
        self.dbClint = dbClint
        self.openAiClint = openAiClint

    


