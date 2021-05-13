from twitter import Twitter, OAuth, TwitterHTTPError
import pymongo
import urllib.parse
import dns
from datetime import datetime
import os

OAUTH_TOKEN=os.environ.get("OAUTH_TOKEN")
OAUTH_SECRET=os.environ.get('OAUTH_SECRET')
CONSUMER_KEY=os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET=os.environ.get('CONSUMER_SECRET')
MONGO_PW=os.environ.get('MONGO_PW')

def search_tweets(q, count=5000):
    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    return t.search.tweets(q=q, result_type='recent', count=count, tweet_mode='extended')

def connect_mdb():
    mongo_url = "mongodb+srv://nicholasjcole:" + urllib.parse.quote(MONGO_PW) + "@app-ideas.kxgdu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_url)
    return client.test

def extract_tweet_data(query_results):
    db = connect_mdb()
    new_tweet_count = 0
    existing_tweet_count = 0
    for status in reversed(query_results['statuses']):
        # get rid of RTs
        if "RT" not in status['full_text']:
            if db.tweet_data.find({"tweet_id":status['id_str']}).count() == 0:
                tweet_id = status['id_str']
                in_reply_to = status['in_reply_to_screen_name']
                in_reply_to_screen_name = status['in_reply_to_screen_name']
                in_reply_to_status_id_str = status['in_reply_to_status_id_str']
                in_reply_to_user_id = status['in_reply_to_user_id']
                in_reply_to_user_id_str = status['in_reply_to_user_id_str']
                is_quote_status = status['is_quote_status']
                lang = status['lang']
                tweet_content = status['full_text']
                tweet_prof_image = status['user']['profile_image_url']
                tweet_prof_name = status['user']['screen_name']
                tweet_actual_name = status['user']['name']
                tweet_create_time = datetime.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                tweet_favorite_count = status['favorite_count']
                tweet_location = status['user']['location']
                tweet_hash_tags = status['entities']['hashtags']
                user_follower_count = status['user']['followers_count']
                user_following_count = status['user']['friends_count']
                user_statuses_count = status['user']['statuses_count']
                user_screen_name = status['user']['screen_name']
                user_id = status['user']['id_str']
                tweet_deleted = "No"
                inserted_date = datetime.now()
                updated_date = datetime.now()
                db.tweet_data.insert({"tweet_id": tweet_id, "in_reply_to": in_reply_to, "in_reply_to_screen_name": in_reply_to_screen_name, "in_reply_to_status_id_str": in_reply_to_status_id_str, "in_reply_to_user_id_str": in_reply_to_user_id_str, "in_reply_to_user_id": in_reply_to_user_id, "is_quote_status": is_quote_status, "lang": lang, "tweet_content": tweet_content, "tweet_prof_image": tweet_prof_image,"tweet_prof_name": tweet_prof_name, "tweet_actual_name": tweet_actual_name, "tweet_create_time": tweet_create_time, "tweet_favorite_count": tweet_favorite_count, "tweet_location": tweet_location, "tweet_hash_tags": tweet_hash_tags, "user_follower_count": user_follower_count, "user_following_count":user_following_count, "user_statuses_count": user_statuses_count, "user_screen_name": user_screen_name, "user_id": user_id, "tweet_deleted": tweet_deleted, "inserted_date":inserted_date, "updated_date":updated_date})
                new_tweet_count += 1
            else:
                existing_tweet_count+=1
    print("{} tweets added and {} tweets already in database".format(new_tweet_count, existing_tweet_count))

if __name__ == "__main__":
    results = search_tweets('"There should be an app" OR "wish there was an app" OR "Someone should build an app" OR "is there an app" OR "need an app that" OR "we need an app for" OR "we need an app that"')
    extract_tweet_data(results)