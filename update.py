#!/usr/bin/env python3
import time

import youtube_search  # from_directory
import youtube_dl
import os
import django
from urllib.request import urlopen

os.environ['DJANGO_SETTINGS_MODULE'] ='ethiomedia.settings'
django.setup()

from client.models import Video
from client.models import Channel
from client.models import Category
from django.utils import timezone
from datetime import datetime, timedelta

import json
import dot_dict
import json
import requests
import time
from django.db.models import Q

credenentials_path = "auth/api.json"
max_result = 10
next_page_token = ''

client_secret = "auth/client_secret.json"
privacy = "private"

published_before = ""

YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video'+"/"+'%(id)s.%(ext)s',
    'noplaylist': False,

}
tmp=datetime.now()-timedelta(days=datetime.today().weekday())
start_date = tmp.replace(hour=0, minute=0,second=0)


saved_videos=Video.objects.filter( Q(publishedAt__gte=start_date)).order_by('-publishedAt')
saved_videoIds=list((o.videoId for o in saved_videos))


def init():

    for x in range(datetime.today().weekday()+1):
        print("Days++++++++++++++++++++++++++++++++++++",datetime.today() + timedelta(-(x)))
        search(next_page_token,datetime.today() + timedelta(-(x)))


    searchFinished()

def searchFinished():
    print("search finished in waiting mode ⏳⏳⏳⏳")
    starttime=time.time()
    while True:
        time.sleep(10800.0 - ((time.time() - starttime) % 10800.0))
        print("Queyring Update Page-----------------------------------------------------------")
        init()



def update(row):
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        video=[]
        try:
            result = ydl.extract_info(
                row['url'],
                download=False
            )
            if 'entries' in result:
                video = result['entries'][0]

            else:
                video = result
                video.pop('id')
        except:
            print('extraction failed')

        Video.objects.all()
        Channel.objects.all()
        Category.objects.all()

        try:
            if video:
                now = datetime.now()
                try:
                    Video.objects.get(videoId=row['videoId'])
                except:
                    print("video does not exist -----")


                det = Video.objects.get(videoId=row['videoId'])
                chn = Channel.objects.get(channelId=row['channelId'])

                det.license=video['license']
                det.view_count=video['view_count']
                det. like_count = video['like_count']
                det.dislike_count =video['dislike_count']
                det.verage_rating = video['average_rating']
                det.lastModified=now
                if  chn.channelStatus=="trusted":
                        det.status='downloaded'
                        det.category=chn.channelCategory
                        det.save()


    #            thumbnails =video['thumbnails']['medium']['url'],
    #            sliderThumbnails =video['thumbnails']['high']['url'],

                det.save()
                print(row['videoId'],"--------------------------------------------------Updated✅✅✅✅")

        except Video.DoesNotExist:
            print('video does not exist')


def search(next_page_token,published_after):
    chn = Channel.objects.filter(channelStatus='trusted').order_by('-channelSubscriberCount')
#    query=['Ethiopian Music','Ethiopian Movie','Ethiopian News','Ethiopian Mezmur']

    chn_list = list(ch.channelTitle for ch in chn)
    querys=chn_list
    #+query

    b={}
    for query in querys:
        print('Querying = '+query)

        b = youtube_search.YoutubeSearch(
                credenentials_path, query, max_result, next_page_token, published_after, published_before)

        new_videos=(o['videoId'] for o in b.response)
        new_videoIds=list(new_videos)


        print("------------------------------------------------------------------")

        for row in b.response:
            if  row['videoId']  in saved_videoIds:
                update(row)


init()