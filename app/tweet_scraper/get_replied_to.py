import tweepy
import os
import app.tweet_scraper.get_app_idea_tweets as gait
import sys
from datetime import datetime

OAUTH_TOKEN=os.environ.get("OAUTH_TOKEN")
OAUTH_SECRET=os.environ.get('OAUTH_SECRET')
CONSUMER_KEY=os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET=os.environ.get('CONSUMER_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)

def retrieve_select_mdb():
    db = gait.connect_mdb()
    # tweets = db.tweet_data.find({"$and": [{"in_reply_to_status_id_str": {"$exists": "true"}}, {"in_reply_to_status_id_str": {"$ne": None}}]})
    tweets = db.tweet_data.find({"$and": [{"in_reply_to_status_id_str": {"$exists": "true"}},
                                          {"in_reply_to_status_id_str": {"$ne": None}},
                                          {"in_reply_to_content": {"$exists": False}}]})
    return tweets

def add_replied_tweet(tweets, limit):
    count = 0
    db = gait.connect_mdb()
    min_limit = min(tweets.count(), limit)
    for tweet in tweets[0:min_limit]:
       try:
            in_reply_to_tweet = get_tweet(tweet['in_reply_to_status_id_str'])
            db.tweet_data.update_one({"tweet_id": tweet['tweet_id']}, {"$set": {"in_reply_to_content": in_reply_to_tweet['full_text']}})
            count+=1
            print("Added {} tweets".format(count))
       except:
           error_msg = sys.exc_info()
           if error_msg[1].__dict__['reason'] == "[{'code': 179, 'message': 'Sorry, you are not authorized to see this status.'}]":
               count += 1
               db.tweet_data.update_one({"tweet_id": tweet['tweet_id']}, {"$set": {"tweet_deleted": "Private"}})
               print("Tweet not found error: {}".format(error_msg[1]))
           elif error_msg[1].__dict__['reason'] == "[{'code': 144, 'message': 'No status found with that ID.'}]":
               count += 1
               db.tweet_data.update_one({"tweet_id": tweet['tweet_id']}, {"$set": {"tweet_deleted": "Deleted"}})
               print("Tweet not found error: {}".format(error_msg[1]))
           else:
               print("Other error: {}".format(error_msg[1]))
    count_text = str(count) + " tweets updated"
    return count_text

def get_tweet(tweet_id):
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    return tweet._json

if __name__ == "__main__":
    tweets = retrieve_select_mdb()
    add_replied_tweet(tweets, 30)
