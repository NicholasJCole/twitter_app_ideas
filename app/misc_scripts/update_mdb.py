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

def retrieve_all_mdb():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find({})
    return tweets

def get_tweet(tweet_id):
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    return tweet._json

def create_updated_dict(tweet):
    tweet_id = tweet['id_str']
    in_reply_to = tweet['in_reply_to_screen_name']
    in_reply_to_screen_name = tweet['in_reply_to_screen_name']
    in_reply_to_status_id_str = tweet['in_reply_to_status_id_str']
    in_reply_to_user_id = tweet['in_reply_to_user_id']
    in_reply_to_user_id_str = tweet['in_reply_to_user_id_str']
    is_quote_status = tweet['is_quote_status']
    lang = tweet['lang']
    tweet_content = tweet['full_text']
    tweet_prof_image = tweet['user']['profile_image_url']
    tweet_prof_name = tweet['user']['screen_name']
    tweet_actual_name = tweet['user']['name']
    tweet_create_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    tweet_favorite_count = tweet['favorite_count']
    tweet_location = tweet['user']['location']
    tweet_hash_tags = tweet['entities']['hashtags']
    user_follower_count = tweet['user']['followers_count']
    user_following_count = tweet['user']['friends_count']
    user_statuses_count = tweet['user']['statuses_count']
    user_screen_name = tweet['user']['screen_name']
    user_id = tweet['user']['id_str']
    tweet_deleted = "No"
    inserted_date = tweet_create_time
    updated_date = datetime.now()
    update_dict = {"tweet_id": tweet_id,
         "in_reply_to": in_reply_to,
         "in_reply_to_screen_name": in_reply_to_screen_name,
         "in_reply_to_status_id_str": in_reply_to_status_id_str,
         "in_reply_to_user_id_str": in_reply_to_user_id_str,
         "in_reply_to_user_id": in_reply_to_user_id,
         "is_quote_status": is_quote_status,
         "lang": lang,
         "tweet_content": tweet_content,
         "tweet_prof_image": tweet_prof_image,
         "tweet_prof_name": tweet_prof_name,
         "tweet_actual_name": tweet_actual_name,
         "tweet_create_time": tweet_create_time,
         "tweet_favorite_count": tweet_favorite_count,
         "tweet_location": tweet_location,
         "tweet_hash_tags": tweet_hash_tags,
         "user_follower_count": user_follower_count,
         "user_following_count": user_following_count,
         "user_statuses_count": user_statuses_count,
         "user_screen_name": user_screen_name,
         "user_id": user_id,
         "tweet_deleted": tweet_deleted,
         "inserted_date": inserted_date,
         "updated_date": updated_date}
    return update_dict

if __name__ == "__main__":
    tweets = retrieve_all_mdb()
    db = gait.connect_mdb()
    count = -1
    # rate limited out at 893
    for tweet in tweets[892:933]:
        try:
            updated_tweet = get_tweet(tweet['tweet_id'])
            updated_dict = create_updated_dict(updated_tweet)
            new_values = {"$set": updated_dict}
            tweet_query = {"tweet_id":updated_dict['tweet_id']}
            db.tweet_data.update_one(tweet_query, new_values)
            count+=1
            print("Number {} tweet refreshed.".format(count))
        except:
            error_msg = sys.exc_info()
            if error_msg[1].__dict__['reason'] == "[{'code': 179, 'message': 'Sorry, you are not authorized to see this status.'}]":
                count+= 1
                db.tweet_data.update_one({"tweet_id":tweet['tweet_id']}, {"$set": {"tweet_deleted":"Private"}})
                print("Tweet not found error: {}".format(error_msg[1]))
            else:
                count+=1
                print("New error: {}".format(error_msg[1]))


