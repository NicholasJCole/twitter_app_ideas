from flask import Flask
import pymongo
import app.tweet_scraper.get_app_idea_tweets as gait
import os
from flask import render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find().sort("tweet_create_time", -1)
    return render_template('index.html', tweets=tweets)

#make pagination for tweets
@app.route("/page")
def paginate():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find({})
    return render_template('index.html', tweets=tweets)

#page for tweets with most favorites
@app.route("/popular")
def popular_tweets():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find().sort("tweet_favorite_count", -1)
    return render_template('index.html', tweets=tweets)