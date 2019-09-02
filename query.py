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
import dot_dict
from urllib.request import urlopen

os.environ['DJANGO_SETTINGS_MODULE'] ='ethiomedia.settings'
django.setup()

from client.models import Video
from client.models import Channel
from client.models import Category
# from client.models import YoutubeComment
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
import com
import urllib


date = datetime.today()
today= datetime.today()
start_week = date - timedelta(date.weekday())
end_week = start_week + timedelta(7)

credenentials_path = "auth/api2.json"
query = "Ethiopian music"
max_result = 2
next_page_token = ''


client_secret = "auth/client_secret2.json"
privacy = "private"
#published_after = "2014-09-21T00:00:00Z"
published_after = date
published_before = ""





YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video'+"/"+'%(id)s.%(ext)s',
    'noplaylist': False,

}
try:
    with open(credenentials_path) as f:
        data = json.load(f)
        api = dot_dict.DotDict(data)
        DEVELOPER_KEY = api.developer_key
        YOUTUBE_API_SERVICE_NAME = api.youtube_api_service_name
        YOUTUBE_API_VERSION = api.youtube_api_version
except:print("Api key path not found in Auth")


dets=[]



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
            response = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id='+row['channelId']+'&key='+DEVELOPER_KEY)
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
            thumbnailsLow =row['thumbnails']['default']['url'],
            thumbnailsHigh =row['thumbnails']['high']['url'],
            thumbnailsMedium =row['thumbnails']['medium']['url'],
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
                    print(row['videoId']+" --------------------------------saved at"+str(datetime.today().now()))

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
        time.sleep(600.0 - ((time.time() - starttime) % 600.0))
        searchCurrent()
        time.sleep()


def get_all_video_in_chn(channel_id):
    videos=[]


    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    part= part="snippet,contentDetails,statistics",

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=5'.format(DEVELOPER_KEY, channel_id)

    url = first_url

    inp = requests.get(url)
    try:
        resp = json.loads(inp.text)

    except:
        print("No video with given channel id")
    try:
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                vid = { **i['id'],**i['snippet'], **{'url':base_video_url + i['id']['videoId']}}
                videos.append(vid)

    except:
        print('no video')

    return videos



comment=""
try:
    with open("comments.txt") as f:

       comment=f.read()
except:print("except")

def searchCurrent():
    try:
        channels = Channel.objects.filter(channelStatus='trusted').order_by('-channelSubscriberCount')

        for chn in channels:
            print('Querying 📺📺📺 =',chn.channelTitle)
            videos=get_all_video_in_chn(chn.channelId)

            for row in videos:

                try:
                    vid = Video.objects.get(videoId=row['videoId'])
                except Video.DoesNotExist:
                    print( "i found it! 😅😅😅",row['videoId'])

                    save(row)
    except:
        print("exception passed")
        pass
    searchFinished()


searchCurrent()
