import os
from dotenv import load_dotenv
from utils.sources.tokenmetrics import TokenMetrics
from utils.db_connectors.firbase import FirebaseClient
from utils.social_conctors.telegramUser import TelegramUserClient
from utils.ai_connectors.open_ai import OpenAIChat
from domain.dataGen.openaigen import OpenAIGen
from domain.dataCollecting.collect_data import CollectDataTodb
from domain.publishing.scheduled import SchaduledMessage
from utils.logging.logginconfig import setup_logger
from domain.dataCollecting.collect_tokenmetrics import CollectDataTokenmetrics
#
load_dotenv()
logging = setup_logger(__name__)

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

tokenMetrics_clint =TokenMetrics()

firbase_clint = FirebaseClient(app_name="missionx",collection_name="telegramMessages")
open_ai_chat_client = OpenAIChat()
# domain clint 
schaduledMessage = SchaduledMessage(telegram_client = telegram_client ,firbase_client = firbase_clint)
collectDataTodb = CollectDataTodb(firbase_client=firbase_clint,telegram_clint=telegram_client)
collectDataTokenmetrics_todb = CollectDataTokenmetrics(tokenmetrics_conector=tokenMetrics_clint,
                                                  db_connector=firbase_clint
                                                  )

openAiGenerator = OpenAIGen(openai_clint=open_ai_chat_client,firbase_clint=firbase_clint)




# Tokenmetrics -------->

def collect_tokenmetric_day_questions_res_tokenAidb():
    try:
        logging.info("Starting to collect _day_questions_res_tokenAi...")
        collectDataTokenmetrics_todb.genrat_day_questions_res_tokenAi()
        logging.info("Finished collecting _day_questions_res_tokenAi.")
    except Exception as e:
        logging.error(f"Error in collect__day_questions_res_tokenAib: {e}")


# Tokenmetrics---> sentiments
def collect_sentiments_data_Tokenmetrics_to_db():
    try:
        logging.info("Starting to collect Telegram data...")
        collectDataTokenmetrics_todb.get_sementem_to_db()
        logging.info("Finished collecting Telegram data.")
    except Exception as e:
        logging.error(f"Error in collect_telegram_byChanel_to_db: {e}")

def genrat_sentiments_data_Tokenmetrics_to_db():
    try:
        logging.info("Starting to collect Telegram data...")
        openAiGenerator.generate_coin_metric_sentims_savedb_step1()
        openAiGenerator.sentiment_to_db_from_db_step2()
        logging.info("Finished collecting Telegram data.")
    except Exception as e:
        logging.error(f"Error in generate_coin_metric_sentims_savedb: {e}")


async def send_teleg_mesg_from_coinmatric_sementim_db():
    try:
        logging.info("Starting to send Telegram messages from DB...")
        await schaduledMessage.send_teleg_mesg_from_coinmatric_sementim_db()
        logging.info("Finished sending Telegram messages from DB.")
    except Exception as e:
        logging.error(f"Error in send_teleg_mesg_from_db: {e}")









# telegram-------------->
        

async def collect_telegram_data_by_chanel_db(chanel_name:str):
    try:
        logging.info("Starting to collect Telegram data...")
        await collectDataTodb.collect_telegram_byChanel_to_db(target_chat_username=chanel_name)
        logging.info("Finished collecting Telegram data.")
    except Exception as e:
        logging.error(f"Error in collect_telegram_byChanel_to_db: {e}")


def generate_telegram_data_db():
    try:
        logging.info("Starting to generate Telegram data...")
        openAiGenerator.get_generate_teleg_savedb()
        
    except Exception as e:
        logging.error(f"Error in get_generate_teleg_savedb: {e}")


async def send_telegram_messages_from_db():
    try:
        logging.info("Starting to send Telegram messages from DB...")
        await schaduledMessage.send_teleg_mesg_from_db()
        logging.info("Finished sending Telegram messages from DB.")
    except Exception as e:
        logging.error(f"Error in send_teleg_mesg_from_db: {e}")

