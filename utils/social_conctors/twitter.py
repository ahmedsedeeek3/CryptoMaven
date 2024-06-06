import os
import json
import logging
import requests
from requests_oauthlib import OAuth1Session
from requests.auth import AuthBase
from utils.logging.logginconfig import setup_logger

# Configure logging
logger = setup_logger(__name__)

class TwitterOAuth:
    def __init__(self, consumer_key, consumer_secret,bearer_token, token_file="twitter_tokens.json"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_file = token_file
        self.access_token = None
        self.access_token_secret = None
        self.bearer_token = bearer_token  # Assumes Bearer token is set as an environment variable
        self.seen_tweet_ids = set()
        self.load_tokens()

    def save_tokens(self, access_token, access_token_secret):
        tokens = {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
        }
        with open(self.token_file, "w") as f:
            json.dump(tokens, f)
        logger.info("Access tokens saved successfully.")

    def load_tokens(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                tokens = json.load(f)
                self.access_token = tokens["access_token"]
                self.access_token_secret = tokens["access_token_secret"]
                logger.info("Access tokens loaded successfully.")

    def fetch_request_token(self):
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)
        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
            logger.info("Request token fetched successfully.")
        except ValueError as e:
            logger.error("There was an issue with the consumer_key or consumer_secret: %s", e)
            raise
        return fetch_response

    def get_authorization_url(self, resource_owner_key):
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret, resource_owner_key=resource_owner_key)
        authorization_url = oauth.authorization_url(base_authorization_url)
        logger.info("Authorization URL generated successfully.")
        return authorization_url

    def fetch_access_token(self, resource_owner_key, resource_owner_secret, verifier):
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        self.access_token = oauth_tokens["oauth_token"]
        self.access_token_secret = oauth_tokens["oauth_token_secret"]
        self.save_tokens(self.access_token, self.access_token_secret)
        logger.info("Access token fetched and saved successfully.")

    def make_request(self, payload):
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )
        response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
        if response.status_code != 201:
            logger.error("Request returned an error: %s %s", response.status_code, response.text)
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
        logger.info("Tweet posted successfully.")
        return response.json()

    def send_message(self, payload):
        if not self.access_token or not self.access_token_secret:
            fetch_response = self.fetch_request_token()
            resource_owner_key = fetch_response.get("oauth_token")
            resource_owner_secret = fetch_response.get("oauth_token_secret")
            
            logger.info("Got OAuth token: %s", resource_owner_key)
            authorization_url = self.get_authorization_url(resource_owner_key)
            logger.info("Please go here and authorize: %s", authorization_url)
            verifier = input("Paste the PIN here: ")
            
            self.fetch_access_token(resource_owner_key, resource_owner_secret, verifier)
        
        json_response = self.make_request(payload)
        logger.info("Response: %s", json.dumps(json_response, indent=4, sort_keys=True))

    def listen_to_tweets(self):
        class BearerAuth(AuthBase):
            def __init__(self, token):
                self.token = token
            def __call__(self, r):
                r.headers["Authorization"] = f"Bearer {self.token}"
                return r
        
        stream_url = "https://api.twitter.com/2/tweets/sample/stream"
        headers = {
            "Content-Type": "application/json",
        }
        auth = BearerAuth(self.bearer_token)  # Use Bearer token for authorization
        params = {
            'tweet.fields': 'created_at,author_id'
        }
        response = requests.get(stream_url, headers=headers, params=params, auth=auth, stream=True)
        if response.status_code != 200:
            logger.error("Request returned an error: %s %s", response.status_code, response.text)
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
        
        logger.info("Listening to tweets...")
        for line in response.iter_lines():
            if line:
                tweet = json.loads(line)
                tweet_id = tweet['data']['id']
                if tweet_id not in self.seen_tweet_ids:
                    self.seen_tweet_ids.add(tweet_id)
                    logger.info("New Tweet received: %s", json.dumps(tweet, indent=4, sort_keys=True))
                    print("New Tweet received: %s" % json.dumps(tweet, indent=4, sort_keys=True))

# def main():
#     consumer_key = os.environ.get("API_KEY")
#     consumer_secret = os.environ.get("API_SECRET_KEY")
    
#     twitter = TwitterOAuth(consumer_key, consumer_secret)
    
#     if not twitter.access_token or not twitter.access_token_secret:
#         fetch_response = twitter.fetch_request_token()
#         resource_owner_key = fetch_response.get("oauth_token")
#         resource_owner_secret = fetch_response.get("oauth_token_secret")
        
#         logger.info("Got OAuth token: %s", resource_owner_key)
#         authorization_url = twitter.get_authorization_url(resource_owner_key)
#         logger.info("Please go here and authorize: %s", authorization_url)
#         verifier = input("Paste the PIN here: ")
        
#         twitter.fetch_access_token(resource_owner_key, resource_owner_secret, verifier)
    
#     payload = {"text": "Hello world!"}
#     twitter.send_message(payload)
    
#     twitter.listen_to_tweets()

# if __name__ == "__main__":
#     main()
