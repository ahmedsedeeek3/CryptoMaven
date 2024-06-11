
class OpenAiPrombet:
    def __init__(self) -> None:
        pass


    def teleg_generator_prombt(self):
        sysROlPrombet = '''            
                    Read the following text and generate an engaging telegram message listing the trending cryptocurrency coins must with
                    their ticker symbols, and price change. Use relevant emojis to make it attractive. add if possible  links or social media references.
                    End with a call to action to follow for hourly insights don't miss any coin @cryptoMissionX.
                    use only price data form the user prombet data .if you miss price never show it never get price for your brain.
                    Tweet Example:
                    🔥 short lovely intro:
                    all coins don't miss any one in list
                    Follow us for hourly insights!
                    formatting should be list ,should use /\n to end line
                    '''
        
        return sysROlPrombet
    

    def twitter_sentiment_generator_prombt(self):
        sysROlPrombet = '''            
                   You are experienced with Twitter and crypto coins. You will take the user's text and turn it into a tweet about the current news.
                     Your target is to enhance user engagement. You shall use only data from the user's prompt.
                     Finish it with a call to action: "Follow my Telegram account to get updates." Use emojis to make the tweet more engaging.
                    '''
        
        return sysROlPrombet