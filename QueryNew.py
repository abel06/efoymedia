#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 01:35:31 2019

@author: parallels
"""


import youtube_search  # from_directory
import youtube_dl
import os
import django
import psutil
from urllib.request import urlopen

os.environ['DJANGO_SETTINGS_MODULE'] ='ethiomedia.settings'
django.setup()

from client.models import Video
from client.models import Channel
from client.models import Category

from django.utils import timezone

#import datetime

from datetime import datetime, timedelta
# from django.contrib.gis.utils import GeoIP
import json
import dot_dict

import json
import requests
import time
from django.db.models import Q

date = datetime.today()
today= datetime.today()
start_week = date - timedelta(date.weekday())
end_week = start_week + timedelta(7)

credenentials_path = "auth/api.json"
query = "Ethiopian music"
max_result = 10
next_page_token = ''


client_secret = "auth/client_secret.json"
privacy = "private"
#published_after = "2014-09-21T00:00:00Z"
published_after = date
published_before = ""





YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video'+"/"+'%(id)s.%(ext)s',
    'noplaylist': False,

}


dets=[]

saved_videos=Video.objects.filter( Q(publishedAt__date=today))
saved_videoIds=list((o.videoId for o in saved_videos))



def save(row):
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
        except:pass


        try:
            cat=Category(category=video['categories'][0])
        except:pass

        if video:
            try:
                cat= Category.objects.get(category=video['categories'][0])
            except Category.DoesNotExist:
                cat.save()

            chn=Channel( channelId = row['channelId'],channelTitle = row['channelTitle'],channelCategory = cat,publishedAt=row['publishedAt'],channelUrl='https://www.youtube.com/channel/'+row['channelId'])
            response = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id='+row['channelId']+'&key=AIzaSyDzZW4RaeAQaHLKyBnhOwZLOAyj4JEmvc0')
            json_data = json.loads(response.text)

            try:
                chn = Channel.objects.get(channelId=row['channelId'])
            except Channel.DoesNotExist:
                chn.channelViewCount=json_data['items'][0]['statistics']['viewCount']
                chn.channelCommentCount=json_data['items'][0]['statistics']['commentCount']
                chn.channelSubscriberCount=json_data['items'][0]['statistics']['subscriberCount']
                chn.channelVideoCount=json_data['items'][0]['statistics']['videoCount']
                chn.save()

            det=Video(
            videoId = row['videoId'],
            channel = chn,
            title = row['title'],
            channelTitle = row['channelTitle'],
            publishedAt =row['publishedAt'],
            thumbnails =row['thumbnails'],
            url = row['url'],
            license = video['license'],
            creator = video['creator'],
            description =video['description'],

            category =cat,
            subtitles = video['subtitles'],
            artist =video['artist'],
            track =video['track'],
            width = video['width'],
            height = video['height'],
            #                resolution = video['resolution'],
            ext =video['ext'],
            duration = video['duration'],
            view_count = video['view_count'],
            like_count = video['like_count'],
            dislike_count =video['dislike_count'],
            average_rating = video['average_rating'],
            status='pending',
            video='https://www.youtube.com/embed/'+ row['videoId'])

            if  chn.channelStatus=="trusted":
                    det.status='downloaded'
                    det.category=chn.channelCategory
                    det.save()
            else:

                 det.save()
            print(row['videoId']+" --------------------------------saved at"+str(datetime.today().now()))



def searchFinished():
    print("Queyring New Released Videos page 🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔🤔")
    for det in dets:
        print("Saving")
        det.save()
    starttime=time.time()
    while True:
        time.sleep(1200.0 - ((time.time() - starttime) % 1200.0))
        searchCurrent()
        time.sleep()


def searchCurrent():
    chn = Channel.objects.filter(channelStatus='trusted').order_by('-channelSubscriberCount')
    query=['Ethiopian Music','Ethiopian Movie','Ethiopian News','Ethiopian Mezmur']
    chn_list = list(ch.channelTitle for ch in chn)
    querys=chn_list+query


    b={}
    for query in querys:
        print('Querying 📺📺📺 = '+query)
        b = youtube_search.YoutubeSearch(
                credenentials_path, query, max_result, '', published_after, published_before)


        new_videos=(o['videoId'] for o in b.response)
        new_videoIds=list(new_videos)
        diff=list(set(new_videoIds) - set(saved_videoIds))
        for row in b.response:
            if row['videoId'] in diff:
                print( "i found it! 😅😅😅" + row['videoId'])
                save(row)

    searchFinished()


searchCurrent()
