
import requests
import os
from utils.logging.logginconfig import setup_logger
from dotenv import load_dotenv

load_dotenv()
api_token = int(os.getenv("TOKEN_MATRIKS"))

url = "https://api.tokenmetrics.com/v2/tokens?token_id=3375%2C3306&token_name=Bitcoin%2C%20Ethereum&symbol=BTC%2CETH&category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=1000&page=0"

headers = {
    "accept": "application/json",
    "api_key": api_token
}

response = requests.get(url, headers=headers)

print(response.text)