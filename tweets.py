import json
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] ='ethiomedia.settings'
django.setup()
from client.models import Tweeter
from client.models import Tweet
import tweepy
import csv
import json
from datetime import datetime, timedelta
import time
with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

def get_tweets(tweeter):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    try:
        tw = api.user_timeline(screen_name=tweeter.tweeterName, count=1,include_rts=False,exclude_replies=True,tweet_mode='extended')

        media_file = ''
        for status in tw:
            media = status.entities.get('media', [])
            if(len(media) > 0):
                media_file=media[0]['media_url']
        if tw:
            try:
                Tweet.objects.get(tweetId=tw[0].id)
                print("tweet exist skipping!!")
            except:
                tweet=Tweet(
                            tweetId=tw[0].id,
                            tweet =tw[0].full_text,
                            tweeter = tweeter,
                            publishedAt =tw[0].created_at,
                            image=media_file,
                            status = 'unpublished')
                tweet.save()
                print("tweet saved successfully")
    except:
        pass

tweeters=Tweeter.objects.filter(status="trusted")

def searchFinished():
    starttime=time.time()
    while True:
        time.sleep(300.0 - ((time.time() - starttime) % 300.0))

        searchCurrent()

def searchCurrent():
    for tweeter in tweeters:
        print(tweeter.tweeterName," Queyring New Released tweets page 🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔")
        get_tweets(tweeter)
    print("Search finished sleeping")
    searchFinished()
searchCurrent()