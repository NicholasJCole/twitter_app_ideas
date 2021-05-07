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
    tweets = db.tweet_data.find({})
    return render_template('index.html', tweets=tweets)

@app.route("/page") #make pagination for tweets
def paginate():
    db = gait.connect_mdb()
    tweets = db.tweet_data.find({})
    return render_template('index.html', tweets=tweets)