#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import dot_dict
import psutil
import django
import os
import youtube_dl
import youtube_search  # from_directory
from django.utils import timezone
from datetime import datetime, timedelta
import json
import requests
import time
from django.db.models import Q
import urllib

os.environ['DJANGO_SETTINGS_MODULE'] = 'ethiomedia.settings'
django.setup()
from client.models import Category
from client.models import Channel
from client.models import Video
from client.models import YoutubeComment
from google.oauth2.credentials import Credentials
import com
import random
import get_comment

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle
"""
Created on Wed May 15 01:35:31 2019

@author: parallels
"""


#import datetime

# from django.contrib.gis.utils import GeoIP


date = datetime.today()
today = datetime.today()
start_week = date - timedelta(date.weekday())
end_week = start_week + timedelta(7)

credenentials_path = "auth/api.json"
query = "Ethiopian music"
max_result = 1
next_page_token = ''


client_secret = "auth/client_secret.json"

privacy = "private"
#published_after = "2014-09-21T00:00:00Z"
published_after = date
published_before = ""

credential = Credentials(
    None,
    refresh_token="1/qIBBS-VbOwfIK3oH2IXZSbkndHQXPV2UvkNNJWVzQvg",
    token_uri="https://accounts.google.com/o/oauth2/token",
    client_id="850077415836-gff6sbf3109v6encr8j6bjhvmup53g73.apps.googleusercontent.com",
    client_secret="amiMrgtybtcSjlKRfBI2DcsU"
)


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
except:
    print("Api key path not found in Auth")


dets = []


def get_all_video_in_chn(channel_id):
    videos=[]


    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    part= part="snippet,contentDetails,statistics",

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=1'.format(DEVELOPER_KEY, channel_id)

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

def startCommenting():
    x=random.randint(1800,3600)
    with open('youtube_build.pkl', 'rb') as input:
        youtube_build = pickle.load(input)

        channels = Channel.objects.filter(
            channelStatus='trusted').order_by('-channelSubscriberCount')

        for chn in channels:
            print('Querying 📺📺📺 =', chn.channelTitle)
            videos = get_all_video_in_chn(chn.channelId)

            for row in videos:
                print("commenting",row['videoId'])

                with open('youtube.pkl', 'rb') as input:
                    youtube_get_obj = pickle.load(input)
                    my_comment1 = get_comment.Comments(chn.channelId,row['videoId'], youtube_get_obj).top_comment

                    my_comment="ዳዉንሎድ ለማረግ የሚከተለውን ዌብሳይት ይጠቀሙ።"
                    n = random.randint(1,len(my_comment))
                    A=my_comment[0:n]
                    B=my_comment[n:-1]

                    # comm=A+" "+"🇼 🇼 🇼⚈🇪 🇫 🇴 🇾 🇲 🇩 🇮 🇦 ⚈ 🇨 🇴 🇲"+B
                    comm= "visit my site"
                    print(comm)
                try:
                    vid = YoutubeComment.objects.get(videoId=row['videoId'])
                    print("comment exist skipping")
                except:
                    request = youtube_build.commentThreads().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "channelId": chn.channelId,
                            "videoId": row['videoId'],
                            "topLevelComment": {
                                "snippet": {
                                    "textOriginal":comm }
                            }
                        }
                    })
                    resp = request.execute()
                    print(resp)

                    det=YoutubeComment(
                         videoId = row['videoId'],
                         channelId = chn.channelId,
                         videoUrl=row['url'],
                         thumbnailsLow=row['thumbnails']['medium']['url'],
                         comment=comm,
                         commentedAt=datetime.today().now()
                        )
                    det.save()
                    print("Done! 😅😅😅 sleeping  ",x,"times  ", row['videoId'])
                    time.sleep(x)



#print(comment)
#resp=com.Comment("UCgdecrMD1EfiqFL_jlnPxvg","otGuN02Ozyw",comment)
startCommenting()
# Video.objects.all().delete()




