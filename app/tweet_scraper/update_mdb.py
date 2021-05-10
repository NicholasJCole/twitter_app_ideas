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

def connect_mdb():
    mongo_url = "mongodb+srv://nicholasjcole:" + urllib.parse.quote(MONGO_PW) + "@app-ideas.kxgdu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_url)
    return client.test

def pull_all_tweets():
    db = connect_mbd()
    tweets = db.tweet_data.find({})
    return tweets

def replace_date(tweets):
    for i in tweets:


