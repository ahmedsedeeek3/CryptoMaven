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
            logger.warning("get_sentiments _get_url return none") 
            return None , None
        return state,data
    

    def get_token_ai_report(self,token_id1,token_id2,symbol1,symbol2):
        # url = "https://api.tokenmetrics.com/v2/ai-reports?token_id=3375%2C3306&symbol=BTC%2CETH&limit=1000&page=0"
        url = f"https://api.tokenmetrics.com/v2/ai-reports?token_id={token_id1}%2C{token_id2}&symbol={symbol1}%2C{symbol2}&limit=1000&page=0"
        state,data = self._get_url(url=url)
        if state is None:
            logger.warning("get_sentiments _get_url return none") 
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


    





# import requests

# url = "https://api.tokenmetrics.com/v2/ai-reports?token_id=3375%2C3306&symbol=BTC%2CETH&limit=1000&page=0"

# headers = {
#     "accept": "application/json",
#     "api_key": "tm-********-****-****-****-************"
# }

# response = requests.get(url, headers=headers)

# # print(response.text)
#     {
#   "success": true,
#   "message": "Data fetched successfully",
#   "length": 2,
#   "data": [
#     {
#       "TOKEN_ID": 3306,
#       "TOKEN_NAME": "Ethereum",
#       "SYMBOL": "ETH",
#       "TRADER_REPORT": "## Introduction\n\nIn this report, we will analyze the quantitative metrics of Ethereum, one of the leading cryptocurrencies, in comparison to Bitcoin. The quantitative metrics provide insights into the risk, return, and overall performance of Ethereum within the crypto market.\n\n## Risk Analysis\n\n- Max Drawdown for Ethereum: -77.0%\n- Max Drawdown for Bitcoin: -79.0%\n- Volatility for Ethereum: 0.56\n\nEthereum has a slightly lower maximum drawdown compared to Bitcoin, indicating relatively lower downside risk. The volatility of Ethereum stands at 0.56, suggesting moderate price fluctuations.\n\n## Return Analysis\n\n- Cumulative return for Ethereum from 2018-02-23: 542.0%\n- Cumulative return for Bitcoin: 324.0%\n- 3-month return for Ethereum: 54.0%\n- 3-month return for Bitcoin: 54.0%\n- 1-year return for Ethereum: 137.0%\n- 1-year return for Bitcoin: 137.0%\n\nEthereum has outperformed Bitcoin in terms of cumulative return since 2018, showing higher returns over various time periods.\n\n## Performance\n\n- Profit factor for Ethereum: 1.13\n- Recovery Factor for Ethereum: 4.19\n- Sharpe Ratio for Ethereum: 0.67\n- Sortino Ratio for Ethereum: 0.97\n- Quantitative Grade: 26.75%\n- Technical Analysis Grade: 10.0%\n- Token Metrics Trader Grade: 13.35% (Combination of Quantitative Grade and Technical Analysis Grade)\n\nEthereum demonstrates a profit factor above 1 and a positive recovery factor, indicating good trading performance. The Sharpe and Sortino ratios suggest a positive risk-adjusted return. The overall quantitative grade for Ethereum is 26.75%, while the technical analysis grade is 10.0%. The Token Metrics Trader Grade combines these scores to provide an overall assessment of 13.35%.\n\n## Conclusion\n\nEthereum presents a strong quantitative profile, with favorable return metrics and risk-adjusted performance. Investors should consider these quantitative metrics alongside other fundamental and technical factors when evaluating investment opportunities in the cryptocurrency market.",
#       "FUNDAMENTAL_REPORT": "## Introduction\n\nEthereum, known for its smart contract functionality, is a leading blockchain platform that has gained significant traction in the crypto space. In this report, we will delve into key fundamental metrics to assess the investment potential of Ethereum.\n\n- ## Community\n\nEthereum boasts an impressive community size and engagement across various social platforms. With a website visit percentile of 100 and a substantial Twitter following of over 3.3 million, it is evident that Ethereum enjoys strong support and interest from the crypto community.\n\n- ## Team and Investors\n\nSurprisingly, Ethereum has no listed employees, presenting a unique aspect compared to traditional companies. However, its decentralized nature and wide developer community contribute to ongoing platform development and innovation.\n\n- ## Tokenomics\n\nEthereum's liquidity ratio, standing at 6.00%, falls within the ideal range of 5% to 50%, indicating healthy liquidity. Moreover, the extensive presence on numerous exchanges, with an impressive exchange score of 100.0%, provides ample trading opportunities for investors.\n\n- ## Competition\n\nAs a pioneer in the smart contract and decentralized applications space, Ethereum faces competition from other blockchain platforms such as Binance Smart Chain, Solana, and Polkadot. It will be crucial for Ethereum to continue innovating to maintain its market leadership.\n\n- ## Volatility and Performance\n\nEthereum's trading volume of $24.4 billion and average daily returns of 196.0% reflect strong market activity and investor interest. The Sortino ratio of 0.96, placing it in the 60.0 percentile, signifies a relatively favorable risk-adjusted performance, although there is room for improvement.\n\n- ## Conclusion\n\nIn conclusion, Ethereum demonstrates robust fundamentals, with strong community support, healthy liquidity, and impressive trading metrics. However, with growing competition and the need to address volatility concerns, Ethereum must continue evolving and adapting to maintain its position as a top blockchain platform. The Token Metrics Fundamental grade of 78.8% further underlines Ethereum's potential but also highlights areas for enhancement and growth.",
#       "TECHNOLOGY_REPORT": "## Development Activity\n- **Total Commits for Github Repo:** 341,023 (Percentile: 10)\n- **Total Forks for Github Repo:** 65,032 (Percentile: 10)\n  \nDevelopment activity is a critical metric for evaluating the progress and evolution of a project. Ethereum's Github repository shows a substantial number of commits and forks, indicating active development and community involvement.\n\n## Audit and Security\n- **Token Audit Relevance:** Outdated\n- **Vulnerabilities:** 26 (Percentile: 6)\n\nEvaluating the audit and security aspects of a blockchain project is crucial to understanding potential risks. Ethereum's outdated token audit relevance and a notable number of vulnerabilities highlight areas that may require attention to enhance the platform's security and robustness.\n\n## Code Quality\n- **Number of Duplicated Blocks:** 111 (Percentile: 7)\n- **Number of Comment Lines:** 11,869 (Percentile: 10)\n- **Bugs:** 4 (Percentile: 3)\n\nCode quality directly impacts the performance and reliability of a blockchain project. Ethereum demonstrates a moderate presence of duplicated blocks, a high volume of comment lines suggesting extensive documentation, and a relatively low number of reported bugs.\n\n## Conclusion\nEthereum's technology metrics suggest a strong development activity with substantial community engagement, along with notable code quality indicators such as extensive documentation and minimal reported bugs. However, the outdated token audit relevance and vulnerabilities highlight areas that may need further attention to enhance security. The overall technology grade of 89.0% reflects a promising foundation with room for improvement in certain areas."
#     },
#     {
#       "TOKEN_ID": 3375,
#       "TOKEN_NAME": "Bitcoin",
#       "SYMBOL": "BTC",
#       "TRADER_REPORT": "## Introduction\n\nIn this report, we will analyze various quantitative metrics for Bitcoin, a prominent cryptocurrency in the market. These metrics will provide insights into the risk, returns, and overall performance of Bitcoin over specific timeframes.\n\n## Risk Analysis\n\n- Max Drawdown: -79.0%\n- Volatility: 0.57\n\nThe Max Drawdown of -79.0% indicates the largest drop in Bitcoin's value from its peak, reflecting the significant risk associated with this asset. The Volatility of 0.57 signifies the fluctuation in Bitcoin's price, highlighting the potential for rapid price movements.\n\n## Return Analysis\n\n- Cumulative return since 2018-01-08: 324.0%\n- 3-month return: 54.0%\n- 1-year return: 137.0%\n\nBitcoin has exhibited substantial returns over different timeframes, showcasing its potential for providing attractive investment returns. The positive returns indicate the profitability of holding Bitcoin during these periods.\n\n## Performance\n\n- Profit factor: 1.12\n- Recovery Factor: 3.69\n- Sharpe Ratio: 0.57\n- Sortino Ratio: 0.83\n- Quantitative Grade: 22.7%\n- Technical Analysis Grade: 31.81%\n- Token Metrics Trader Grade: 29.99%\n\nThe Profit Factor of 1.12 indicates that the profits generated by Bitcoin have outweighed the losses, albeit marginally. The Recovery Factor of 3.69 signifies that Bitcoin has recovered more than three times the risk-adjusted losses.\n\nThe Sharpe Ratio of 0.57 and Sortino Ratio of 0.83 provide insights into the risk-adjusted returns of Bitcoin, with higher values indicating better risk-adjusted performance.\n\nThe Quantitative Grade, Technical Analysis Grade, and Token Metrics Trader Grade provide a comprehensive evaluation of Bitcoin's performance based on quantitative and technical factors. It reflects a combined assessment of the asset's quantitative metrics and technical analysis results.\n\n## Conclusion\n\nIn conclusion, Bitcoin has demonstrated significant returns over various timeframes, with notable risk factors such as high volatility and drawdown. The quantitative metrics suggest a moderately positive outlook for Bitcoin, with the Token Metrics Trader Grade combining both quantitative and technical analysis aspects to provide a holistic view of the asset's performance in the market. It is essential to consider these quantitative metrics alongside other fundamental analysis factors when evaluating investments in Bitcoin.",
#       "FUNDAMENTAL_REPORT": "## Introduction\n\nBitcoin is the pioneer cryptocurrency that introduced the concept of decentralized digital money to the world. With a market capitalization surpassing other cryptocurrencies by a significant margin, Bitcoin plays a crucial role in the broader crypto ecosystem. In this investment report, we will analyze the fundamental metrics of Bitcoin to gain insights into its current standing and potential for future growth.\n\n- ## Community\n\nBitcoin has a strong and vibrant community of supporters, as reflected in its impressive metrics across various social media platforms. The website visits and Twitter followers in the 100th percentile indicate a high level of interest and engagement from users and investors. While the lack of Youtube views and employees may seem unorthodox, Bitcoin's decentralized nature and community-driven development model contribute to its unique appeal.\n\n- ## Team and Investors\n\nBitcoin operates without a central team or dedicated employees, as it was created anonymously by the pseudonymous figure Satoshi Nakamoto. The lack of a formal team structure may raise some concerns about ongoing development and support. However, Bitcoin's widespread adoption and network effects have attracted prominent investors and supporters from both institutional and retail sectors.\n\n- ## Tokenomics\n\nWith a circulating supply percentile of 100.0%, Bitcoin demonstrates a high level of distribution and liquidity in the market. The tokenomics of Bitcoin are designed to be deflationary, with a capped supply of 21 million coins. This scarcity model has contributed to Bitcoin's status as a store of value and digital gold within the crypto ecosystem.\n\n- ## Competition\n\nBitcoin faces competition from various other cryptocurrencies and digital assets that aim to improve upon its perceived shortcomings, such as scalability and transaction speed. Despite this competition, Bitcoin maintains its dominant position in the market due to its first-mover advantage, network effects, and brand recognition.\n\n- ##  Volatility and Performance\n\nBitcoin's liquidity ratio falling below the ideal range of 5% to 50% highlights the potential risk associated with market volatility and price fluctuations. However, its high trading volume and exchange score of 100.0% indicate robust market activity and demand for the asset. The Sortino ratio, while not in the top percentile, showcases a reasonable risk-adjusted return profile for investors.\n\n- ## Conclusion\n\nIn conclusion, Bitcoin remains a central player in the cryptocurrency space, with a strong community, widespread adoption, and solid fundamentals. While the lack of a formal team structure and low liquidity ratio present some challenges, Bitcoin's proven track record, tokenomics, and market dominance position it as a resilient and valuable asset. With a Token Metrics Fundamental grade of 72.6%, Bitcoin continues to be a compelling investment opportunity for both institutional and retail investors seeking exposure to the digital asset class.",
#       "TECHNOLOGY_REPORT": "## Development Activity\n\n  - Total Commits for Github Repo: 40745 (Percentile: 8)\n  - Total Forks for Github Repo: 39237 (Percentile: 10)\n\nThe Bitcoin project has shown significant development activity with a high number of commits and forks on its Github repository. This demonstrates continuous work on the project and strong community engagement.\n\n- ## Audit and Security\n\n  - Token Audit Relevance: Outdated\n  - Bugs: 42 (Percentile: 5)\n  - Vulnerabilities: 0 (Percentile: 0)\n\nThe token audit relevance being outdated raises concerns regarding the security and reliability of the project. However, the low number of vulnerabilities is a positive sign for the security of the platform, despite the presence of some bugs.\n\n- ## Code Quality\n\n  - Number of Duplicated Blocks in the code: 14 (Percentile: 3)\n  - Number of Comment Lines in the code: 9476 (Percentile: 10)\n\nThe low number of duplicated blocks in the code indicates good code quality, while the high number of comment lines suggests well-documented codebase, which can aid in understanding and maintaining the project.\n\n- ## Conclusion\n\nThe technology metrics for Bitcoin present a mixed picture. While there is strong development activity and high community engagement, the outdated token audit relevance is a concern. Additionally, the presence of bugs, although not critical, needs to be addressed. However, the codebase quality in terms of duplications and comments is satisfactory.\n\nThe overall technology grade for Bitcoin based on the provided metrics is 85.0%, reflecting a solid foundation with room for improvement in certain areas to enhance security and reliability."
#     }
#   ]
# }