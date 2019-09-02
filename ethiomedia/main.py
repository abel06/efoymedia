import youtube_search  # from_directory
import youtube_dl

import django
django.setup()

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'EthioMedia.settings'

from polls.models import Video

credenentials_path = "auth/api.json"
query = "New Amharic Music"
max_result = 20
next_page_token = ''

description = ""
playlist = "Mezmur"
category = "Entertainment"
client_secret = "auth/client_secret.json"
privacy = "private"
published_after = "2014-09-21T00:00:00Z"
published_before = ""


def search():
    b = youtube_search.YoutubeSearch(
        credenentials_path, query, max_result, next_page_token, '', published_before)
    return b.response
#published_after

YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video'+"/"+'%(id)s.%(ext)s',
    'noplaylist': False,

}

#'dateafter': '20190101'
response = search()


def update(row, key, value):
    row.update({key: value})


with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    for row in response:

        result = ydl.extract_info(
            row['url'],
            download=False
        )
        if 'entries' in result:
            video = result['entries'][0]

        else:
            video = result
            video.pop('id')
        row.update({'license': video['license']})
        row.update({'creator': video['creator']})
        row.update({'description': video['description']})
        row.update({'categories': video['categories']})
        row.update({'subtitles': video['subtitles']})
        row.update({'artist': video['artist']})
        row.update({'track': video['track']})
        row.update({'width': video['width']})
        row.update({'height': video['height']})
        row.update({'resolution': video['resolution']})
        row.update({'ext': video['ext']})
        row.update({'duration': video['duration']})
        row.update({'view_count': video['view_count']})
        row.update({'like_count': video['like_count']})
        row.update({'dislike_count': video['dislike_count']})
        row.update({'average_rating': video['average_rating']})


#        row.update(video['view_count'])


#print(response[0].keys())
print(response[0]['dislike_count'])
for resp in response:
    Video.objects.all()
    det = Video(videoId = resp['videoId'],
    channelId = resp['channelId'],
    title = resp['title'],
    channelTitle = resp['channelTitle'],
    publishedAt =resp['publishedAt'],
    thumbnails =resp['thumbnails'],
    url = resp['url'],
    license = resp['license'],
    creator = resp['creator'],
    description =resp['description'],
    categories = resp['categories'],
    subtitles = resp['subtitles'],
    artist =resp['artist'],
    track =resp['track'],
    width = resp['width'],
    height = resp['height'],
    resolution = resp['resolution'],
    ext =resp['ext'],
    duration = resp['duration'],
    view_count = resp['view_count'],
    like_count = resp['like_count'],
    dislike_count =resp['dislike_count'],
    average_rating = resp['average_rating'],)


    try:
        det = Video.objects.get(videoId=resp['videoId'])
    except Video.DoesNotExist:
        det.save()


print(response[0].keys())
