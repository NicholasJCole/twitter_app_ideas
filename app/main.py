from flask import Flask
import pymongo
import tweet_scraper.get_app_idea_tweets as gait
import os

MONGO_PW=os.environ.get('MONGO_PW')

app = Flask(__name__)

@app.route("/")
def home_view():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find({}).limit(10)
    return "<h1>Test app</h1>"