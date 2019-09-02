import os
import django
import psutil
import dot_dict
from urllib.request import urlopen

os.environ['DJANGO_SETTINGS_MODULE'] ='ethiomedia.settings'
django.setup()

from client.models import Tweeter
from client.models import Tweet
from client.models import Category
import tweepy
import csv
import json
from datetime import datetime, timedelta
from TwitterSearch import *
import time

def get_tweeters():
    cat=Category.objects.filter(category="General")[0]
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['Addis Ababa']) # let's define all words we would like to have a look for
        # tso.set_language('am') # we want to see German tweets only
        tso.set_include_entities(False) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = '83BeByPed65Uc3Cu0t7lXaxon',
            consumer_secret = 'HzOefqLkkejFrUSAoT4fyLufqN9cOrpbQ6gPFgX2R769VhXMO6',
            access_token = '1263740724-TolpJ8rMORTRsA5n30dnXWPgBH1OxorBANYjWYZ',
            access_token_secret = 'hr6FAsIo6vqx2uBw04DvqeRpzkcJwST0lEv0G3KoTjYIr'
         )


         # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tso):

            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            image=""
            try:
                image=tweet['user']['profile_banner_url']

            except:
                pass

            try:
                Tweeter.objects.get(tweeterName=tweet['user']['screen_name'])
                print(tweet['user']['screen_name']," Tweeter exist skipping!")

            except:
                tweeter=Tweeter(
                    tweeterName = tweet['user']['screen_name'],
                    status="unset",
                    url="https://twitter.com/"+tweet['user']['screen_name'],
                    publishedAt = datetime.today().now(),
                    followers_count=tweet['user']['followers_count'],
                    statuses_count =tweet['user']['statuses_count'],
                    description =tweet['user']['description'],
                    category=Category.objects.filter(category="General")[0],
                    location =tweet['user']['location'],
                    image =image
                )
                tweeter.save()
                print(tweet['user']['screen_name']," Tweeter added successfully!")


    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
get_tweeters()