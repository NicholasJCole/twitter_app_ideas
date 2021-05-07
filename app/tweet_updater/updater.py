import tweepy
import os

OAUTH_TOKEN=os.environ.get("OAUTH_TOKEN")
OAUTH_SECRET=os.environ.get('OAUTH_SECRET')
CONSUMER_KEY=os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET=os.environ.get('CONSUMER_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)

def get_tweet(tweet_id):
    tweet = api.get_status(id_of_tweet)
    return tweet


