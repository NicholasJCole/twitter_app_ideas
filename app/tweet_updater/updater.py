import tweepy
import os
import app.tweet_scraper.get_app_idea_tweets as gait

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
    tweet = api.get_status(id_of_tweet)
    return tweet

def update_tweet(tweet):
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
    inserted_date = datetime.now()
    updated_date = datetime.now()
    db.tweet_data.insert(
        {"tweet_id": tweet_id,
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
         "updated_date": updated_date})
