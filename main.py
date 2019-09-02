
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

#import datetime

from datetime import datetime, timedelta
# from django.contrib.gis.utils import GeoIP
import json
import dot_dict

import json
import requests
import time
import psutil


date = datetime.today()
start_week = date - timedelta(date.weekday())
end_week = start_week + timedelta(7)

credenentials_path = "auth/api.json"
query = "Ethiopian music"
max_result = 50
next_page_token = ''

description = ""
playlist = "Mezmur"
category = "Entertainment"
client_secret = "auth/client_secret.json"
privacy = "private"
#published_after = "2014-09-21T00:00:00Z"
published_after = start_week
published_before = ""





YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video'+"/"+'%(id)s.%(ext)s',
    'noplaylist': False,

}








def update(row, key, value):
    row.update({key: value})
def updateDB(det):
    try:
        det = Video.objects.get(videoId=row['videoId'])
    except Video.DoesNotExist:
        det.save()



def searchUpdateFinished(next_page_token):
    starttime=time.time()
    while True:
        time.sleep(1800.0 - ((time.time() - starttime) % 1800.0))
        print("Queyring Update Page-----------------------------------------------------------")
        search(next_page_token)
        time.sleep()

#response = search()
def process(response):
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        for row in response:
                cpu=psutil.cpu_percent()
                # gives an object with many fields
                psutil.virtual_memory()
                # you can convert that object to a dictionary
                a=dict(psutil.virtual_memory()._asdict())
                print(cpu)

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

                Video.objects.all()
                Channel.objects.all()
                Category.objects.all()

                try:
                    cat=Category(category=video['categories'][0])
                except:pass

                try:
                    if video:
                        now = datetime.now()

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

                        det.save()
                        print('Updating....'+row['title'])
                except Video.DoesNotExist:

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
                            chn.channelViewCount=json_data['items'][0]['statistics']['viewCount']
                            chn.channelCommentCount=json_data['items'][0]['statistics']['commentCount']
                            chn.channelSubscriberCount=json_data['items'][0]['statistics']['subscriberCount']
                            chn.channelVideoCount=json_data['items'][0]['statistics']['videoCount']
                            chn.save()




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
                        print("Channel Status = "+chn.channelStatus)
                        det.save()
                        print('video Saved' +row['title'])



def search(next_page_token):
    print('Next '+next_page_token)

    chn = Channel.objects.filter(channelStatus='trusted')
    chn_list=[]
    querys=['Ethiopian Music','Ethiopian Movie','Ethiopian News','Ethiopian Mezmur']
    for ch in chn:
        chn_list.append(ch.channelTitle)

    querys=querys+chn_list

    b={}
    for query in querys:
        print('Querying = '+query)
        b = youtube_search.YoutubeSearch(
                credenentials_path, query, max_result, next_page_token, published_after, published_before)
        process(b.response)

    if b:
#        search(b.response[0]['nextPageToken'])
        searchUpdateFinished(b.response[0]['nextPageToken'])
    else:
        searchUpdateFinished(next_page_token)



search(next_page_token)

