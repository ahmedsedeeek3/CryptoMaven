import os
import time
import json
import requests
from utils.logging.logginconfig import setup_logger
from dotenv import load_dotenv

load_dotenv()

logger = setup_logger(__name__)


# url = "https://api.tokenmetrics.com/v2/sentiments?limit=1000&page=0"
# url = "https://api.tokenmetrics.com/v2/quantmetrics?token_id=3375%2C3306&symbol=BTC%2CETH&category=layer-1%2Cnft&exchange=binance%2Cgate&marketcap=100000000&volume=100000000&fdv=100000000&limit=1000&page=0"
# url = "https://api.tokenmetrics.com/v2/correlation?token_id=3375%2C3306&symbol=BTC%2CETH&category=layer-1%2Cnft&exchange=gate%2Cbinance&limit=1000&page=0"
# url = "https://api.tokenmetrics.com/v2/all-trend-indicators?token_id=3375%2C3306&symbol=BTC%2CETH&indicator=mama%2Cmom&startDate=2023-10-01&endDate=2023-10-10&limit=1000&page=0"
# url = "https://api.tokenmetrics.com/v2/token-details-price-charts?token_id=3375&category=trader&timeFrame=MAX&chartFilters=price%2Ctrader_grade%2Cbullish%2Cbearish"
# url = "https://api.tokenmetrics.com/v2/indices-index-allocation-charts?category=trader"
# url = "https://api.tokenmetrics.com/v2/indices-roi-charts?category=trader&timeFrame=MAX&chartFilters=backtested_roi%2C%20index_roi%2Cbtc_roi%2Ctotal_market_roi"
# url = "https://api.tokenmetrics.com/v2/market-percent-of-bullish-vs-bearish-charts"
# url = "https://api.tokenmetrics.com/v2/market-bull-and-bear-charts"
# url = "https://api.tokenmetrics.com/v2/market-percent-of-bullish-tm-grades?timeFrame=Y&chartFilters=total_crypto_market%2C%20%20percent_of_bullish_tm_grades"
# url = "https://api.tokenmetrics.com/v2/market-tm-grade-signal?timeFrame=Y&chartFilters=total_crypto_market%2C%20%20bullish%2C%20bearish"
# url = "https://api.tokenmetrics.com/v2/bitcoin-vs-altcoin-season-charts?timeFrame=Y&chartFilters=altcoin_indicator%2Caltcoin_season%2Cbitcoin_season"
# url = "https://api.tokenmetrics.com/v2/annualized-historical-volatility-charts?timeFrame=MAX&chartFilters=market_cap%2C%20volatility_index%2C%2090th_percentile%2C%2010th_percentile"
# url = "https://api.tokenmetrics.com/v2/total-market-crypto-cap-charts?timeFrame=MAX&chartFilters=total_market_cap%2Caltcoin_market_cap%2Cbtc_market_cap"
# url = "https://api.tokenmetrics.com/v2/market-movers-charts?chartFilters=negativeDailyPricePercentageChange%2CpositiveDailyPricePercentageChange"


# headers = {
#     "accept": "application/json",
#     "api_key": api_token
# }

# response = requests.get(url, headers=headers)

# print(response.text)









class TokenMetrics:
    def __init__(self) -> None:
        self.api_token = os.getenv("TOKEN_MATRIKS") 


        
    def token_metrics_chat_bot(self, text, max_retries=5, backoff_factor=2.5):
        url = "https://api.tokenmetrics.com/v2/tmai"
        payload = {"messages": [{"user": text}]}
        headers = {
            "accept": "application/json",
            "api_key": self.api_token,
            "content-type": "application/json"
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes

                json_res = response.json()
                
                if "success" not in json_res or "answer" not in json_res  :
                    logger.warning(f"Expected keys 'success' and 'answer' not found in 'text': {json_res}")
                    return None, None
                
                json_res_text = json_res["answer"]
                

                return json_res["success"], json_res_text

            except requests.exceptions.RequestException as e:
                if response.status_code == 429:
                    retry_after = backoff_factor * (2 ** attempt)
                    logger.warning(f"HTTP error occurred: {e}. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    logger.warning(f"HTTP error occurred: {e}")
                    break
            except ValueError as e:
                logger.warning(f"JSON parsing error: {e} - Response: {response.text if response else 'No response'}")
                break
            except Exception as e:
                logger.warning(f"An unexpected error occurred: {e}")
                break

        return None, None

    def get_sentiments(self):
        url = "https://api.tokenmetrics.com/v2/sentiments?limit=1000&page=0"
        state,data = self._get_url(url=url)
        if state is None:
            logger.warning(f"get_sentiments _get_url return none") 
            return None , None
        return state,data
    

    def _get_url(self, url, max_retries=5, backoff_factor=2.5):
        
        headers = {
            "accept": "application/json",
            "api_key": self.api_token,
            "content-type": "application/json"
        }

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes

                json_res = response.json()
                
                if "success" not in json_res or "data" not in json_res  :
                    logger.warning(f"Expected keys 'success' and 'data' not found in 'text': {json_res}")
                    return None, None
                
                json_res_text = json_res["data"]
                

                return json_res["success"], json_res_text

            except requests.exceptions.RequestException as e:
                if response.status_code == 429:
                    retry_after = backoff_factor * (2 ** attempt)
                    logger.warning(f"HTTP error occurred: {e}. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    logger.warning(f"HTTP error occurred: {e}")
                    break
            except ValueError as e:
                logger.warning(f"JSON parsing error: {e} - Response: {response.text if response else 'No response'}")
                break
            except Exception as e:
                logger.warning(f"An unexpected error occurred: {e}")
                break

        return None, None


    

