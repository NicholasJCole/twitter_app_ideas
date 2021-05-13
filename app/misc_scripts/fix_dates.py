import sys
from datetime import datetime


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)

def retrieve_all_mdb():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find({})
    return tweets

if __name__ == "__main__":
    tweets = retrieve_all_mdb()
    db = gait.connect_mdb()
    for tweet in tweets:
        if type(tweet['tweet_create_time']) == str:
            updated_tweet_create_time = datetime.strptime(tweet['tweet_create_time'],'%a %b %d %H:%M:%S +0000 %Y')
            print(updated_tweet_create_time) , " Tweet ID" , print(tweet['tweet_id'])
            db.tweet_data.update_one({"tweet_id": tweet['tweet_id']}, {"$set": {"tweet_create_time": updated_tweet_create_time}})

