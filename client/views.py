from django.urls import resolve
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Video, Channel, Section, Page, Viewer, FacebookPost, RadioStation, Tweet, Tweeter
from client.serializers import UserSerializer, GroupSerializer, VideoSerializer, FacebookPostSerializer
from rest_framework import viewsets
from django.template import loader
from django.http import HttpResponse

from django.db.models import Q
from datetime import datetime, timedelta
# from django.contrib.gis.utils import GeoIP
from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import maxminddb
from django.conf import settings  # correct way
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import youtube_dl
import json
import requests
import youtube_search
import uuid
from django.db.models import F
from itertools import chain
import random
from django.middleware.gzip import GZipMiddleware
from django.views.decorators.gzip import gzip_page
from rest_framework import generics
from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
import django_filters
gzip_middleware = GZipMiddleware()

# def top(category):
#     top_list=[]
#     for x in range(7,60,7):
#         top_list =  Video.objects.filter(
#     Q(channel__channelCategory=category) & Q(publishedAt__gte=now-timedelta(days=x)) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')
#         if top_list:
#             break

#     return top_list


GEOIP_PATH = settings.GEOIP_PATH

date = datetime.today()
start_week = date - timedelta(date.weekday())
end_week = start_week + timedelta(7)


now = datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)


reader = maxminddb.open_database(GEOIP_PATH+'/GeoLite2-City.mmdb')

latest_video_list = Video.objects.order_by('publishedAt')
sections = Section.objects.all().exclude(category='Live')
pages = Page.objects.all()

# to response fast its taken out from index view

top_list = []
# Video.objects.filter(Q(publishedAt__gte=now-timedelta(days=datetime.today().weekday())) & (
#     Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')

BLOCKED_BROWSERS = []
# 'AhrefsBot','BLEXBot','YandexBot','DotBot','Nimbostratus-Bot','GrapeshotCrawler'
top_video = []
latests = []
for page in pages:
    tmp = []
    for x in range(7, 60, 7):
        tmp = Video.objects.filter(
            Q(publishedAt__gte=now-timedelta(days=x)) & Q(channel__channelCategory=page.category) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')[:2]
        top_list = list(chain(top_list, tmp))

        if tmp:
            top_video.append(
                {'name': page.link, 'title': page.title, 'data': tmp[0]})
            break


for page in pages:
    ltmp = Video.objects.filter(
        Q(publishedAt__gte=now-timedelta(days=x)) & Q(channel__channelCategory=page.category) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-publishedAt')[:1]
    print(ltmp)
    if ltmp:
        latests.append(
            {'name': page.link, 'title': page.title, 'data': ltmp[0]})

template = loader.get_template('index.html')

output = ', '.join([q.videoId for q in latest_video_list])


def saveViewer(request):
    if request:
        continent = ""
        country = ""
        timezone = ""
        city = ""
        user = ""
        ip = ""
        location = ""
        try:
            ip = request.META['HTTP_X_REAL_IP']
        except:
            pass
        try:
            location = reader.get(request.META['HTTP_X_REAL_IP'])
        except:
            pass
        try:
            continent = location['continent']['code']
        except:
            pass
        try:
            country = location['country']['names']['en']
        except:
            pass
        try:
            timezone = location['location']['time_zone']
        except:
            pass
        try:
            city = location['city']['names']['en']
        except:
            pass
        try:
            user = request.META['HTTP_USER_AGENT']
        except:
            pass

        try:
            viewer = Viewer.objects.get(user=user, browser=request.user_agent.browser.family,
                                        browser_version=request.user_agent.browser.version_string,
                                        os=request.user_agent.os.family,
                                        os_version=request.user_agent.os.version_string,
                                        device=request.user_agent.device.family,
                                        ip=ip,
                                        country=country,
                                        timezone=timezone,
                                        city=city)
            viewer.view_count = int(viewer.view_count)+1
            viewer.save()

        except:
            obj, created = Viewer.objects.update_or_create(
                user=user,
                browser=request.user_agent.browser.family,
                browser_version=request.user_agent.browser.version_string,
                os=request.user_agent.os.family,
                os_version=request.user_agent.os.version_string,
                device=request.user_agent.device.family,
                ip=ip,
                country=country,
                timezone=timezone,
                city=city,
                view_count=1,
                defaults={"lastVisitAt": datetime.now()}
            )
            obj.save()

    #     # except:print("except")


def allowed(request):
    if request:
        continent = ""
        country = ""
        timezone = ""
        city = ""
        user = ""
        ip = ""
        location = ""
        try:
            ip = request.META['HTTP_X_REAL_IP']
            viewer = Viewer.objects.filter(Q(ip=ip) & Q(status='blocked'))
            print("viewer", viewer)

            if viewer:
                return false
            else:
                return True
        except:
            return True
        try:
            if request.user_agent.browser.family in BLOCKED_BROWSERS:
                return False
            else:
                return True
        except:
            return True


def video(category, request):

    video_list = Video.objects.filter(
        Q(channel__channelCategory=category) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-publishedAt')
    page = request.GET.get('page', 1)
    paginator = Paginator(video_list, 24)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return videos


@require_http_methods("GET")
@gzip_page
def index(request):

    tops_of_the_week = Video.objects.filter(Q(publishedAt__gte=now-timedelta(days=x)) & (
        Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')[:5]

    data_list = []

    for section in sections:
        data_list.append({'section_title': section.title,
                          'video_list': video(section.category, request)[:10]})

    # device_type=''
    # if request.user_agent.is_mobile:
    #     device_type="mobile"

    context = {'data_list': data_list,
               'top_list': top_list[:45],
               'tops_of_the_week': latests,
               'active': 'home',
               'meta': top_video[0],
               'musics': video("Music", request)[:10],
               }

    # if not allowed(request):
    #     return
    # else:
    #     pass

    # saveViewer(request)
    # context = {"tops_of_the_week": tops_of_the_week}

    return HttpResponse(template.render(context, request))
    # return gzip_middleware.process_response(context, request)


@require_http_methods("GET")
def view(request):

    name = request.resolver_match.url_name
    pages = Page.objects.filter(category=name)

    page_title = ''
    top_list = []
    # top(name)

    if pages:
        page_title = pages[0]
    template = loader.get_template('list.html')
    # context = {
    #     'data_list': [{
    #         'title': page_title,
    #         'video_list': video(name, request)
    #     }
    #     ], 'top_list': top_list,
    #     'tops_of_the_week': [{'name': pages[0].link, 'title': pages[0].title, 'data':video(name, request)[0]}], 'active': pages[0].link,
    #     'meta': top_list[0]
    # }
    # 'tops_of_the_week': [{'name': pages[0].link, 'title': pages[0].title, 'data':top_list[0]}], 'active': pages[0].link,

    # if not allowed(request):
    #     return
    # else:
    #     pass

    # saveViewer(request)
    print("name", name)

    top_list = Video.objects.filter(
        Q(channel__channelCategory=name) & Q(publishedAt__gte=now-timedelta(days=x)) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')
    context = {
        'video_list': video(name, request),
        'cat': name,
        'top_list': top_list

    }
    return HttpResponse(template.render(context, request))


def list_view(request):
    category = request.GET.get("category")
    context = {
        'video_list': video(category, request)
    }
    template = loader.get_template('listview.html')
    return HttpResponse(template.render(context, request))


def auto_complete(request):

    query = request.GET.get('search')

    inp = requests.get(
        "http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q="+query)

    whileset = set("()")
    tmp = ""
    for i in inp.text[18:]:
        if i not in whileset:
            tmp += i

    resp = json.loads(tmp)
    return JsonResponse({"result": resp})


def search_youtube(request):
    query = request.GET.get('search')

    b = {}
    if query:
        b = youtube_search.YoutubeSearch(
            settings.CREDENTIALS_PATH, query, 50, '', '', 'date').response

    top_list = Video.objects.filter(Q(publishedAt__gte=now-timedelta(days=datetime.today().weekday())) & (
        Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')

    context = {
        'video_list': b,
        'top_list': top_list[:10],
    }
    template = loader.get_template('search.html')
    return HttpResponse(template.render(context, request))


def get_all_video_in_chn(query):
    videos = []

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    part = part = "snippet,contentDetails,statistics",

    first_url = base_search_url + \
        'key={}&query={}&part=snippet,id&order=date&maxResults=5'.format(
            'AIzaSyDzZW4RaeAQaHLKyBnhOwZLOAyj4JEmvc0', query)

    url = first_url

    inp = requests.get(url)
    resp = json.loads(inp.text)
    try:
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                vid = {**i['id'], **i['snippet'], **
                       {'url': base_video_url + i['id']['videoId']}}
                videos.append(vid)

    except:
        print('no video')

    return videos


def my_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))

    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


def download_youtube(request):

    YDL_OPTIONS = {
        'format': 'bestvideo',
        'outtmpl': 'video'+"/"+'%(id)s.%(ext)s',
        'audioformat': "mp3",
        'noplaylist': True,
        'outtmpl': settings.MEDIA_ROOT + "/"+'%(id)s',
        'progress_hooks': [my_hook]

    }
    vid_url = request.GET.get('download')
    print("vid url %%%%%%%%%%%%%%%%%%", vid_url)

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        video = []
        try:
            result = ydl.extract_info(
                vid_url,
                download=False
            )
            if 'entries' in result:
                video = result['entries'][0]

            else:
                video = result

        except:
            pass

    print(video)
    formats = video['formats']
    url = ""
    ext = ""
    abr = 0
    for format in formats:
        url = format["url"]
        ext = format["ext"]
        print(format)
        if format['acodec'] == "opus":
            if int(format['abr']) > abr:
                abr = int(format['abr'])

    print("abr--------00000000000 ==", abr)

    print('inside download-----------------------------------', url
          )

    # return JsonResponse({"filename": video['id']+video['ext']})
    return JsonResponse({"filename": url, "name": video['id']})


def redirect_video(request):
    videoId = request.GET.get('videoId')
    top_video = []
    redirected_video = False
    if videoId:
        vid = Video.objects.filter(videoId=videoId)
        top_video = vid[0]
        channelId = vid[0].channel.channelId

        video_list = Video.objects.filter(
            Q(channel__channelCategory=vid[0].channel.channelCategory) & (Q(status='downloaded') | Q(channel__channelStatus='trusted')))
        vids = vid.union(video_list)
        redirected_video = True

    else:
        cat = request.GET.get('category', 1)
        vids = Video.objects.filter(
            Q(channel__channelCategory=cat) & (Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')
        x = random.randint(0, 23)
        if vids:
            top_video = vids[x]
        redirected_video = False

    page = request.GET.get('page', 1)
    paginator = Paginator(vids, 24)
    # try:
    videos = paginator.page(page)
    print(videos)
    # except PageNotAnInteger:
    #     videos = paginator.page(1)
    # except EmptyPage:
    #     videos = paginator.page(paginator.num_pages)

    context = {
        'video_list': videos,
        'top_list': vids[:10],
        'meta': top_video,
        'redirected_video': redirected_video
    }
    template = loader.get_template('redirect.html')
    return HttpResponse(template.render(context, request))


def radio_view(request):

    template = loader.get_template("radio.html")
    stations = RadioStation.objects.filter(Q(status='published'))
    tweet_list = Tweet.objects.all().order_by("-publishedAt")
    page = request.GET.get('page', 1)
    paginator = Paginator(tweet_list, 10)
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)

    context = {
        'tweets': tweets,
        "stations": stations
    }

    return HttpResponse(template.render(context, request))


def tmp_view(request):

    name = request.resolver_match.url_name
    pages = Page.objects.filter(category=name)

    page_title = ''
    top_list = Video.objects.filter(Q(publishedAt__gte=now-timedelta(days=7)) & Q(channel__channelCategory=name) & (
        Q(status='downloaded') | Q(channel__channelStatus='trusted'))).order_by('-view_count')

    if pages:
        page_title = pages[0]
    template = loader.get_template('list.html')

    context = {
        'data_list': [{
            'title': page_title,
            'video_list': video(name, request)
        }
        ], 'top_list': top_list,
        'tops_of_the_week': [{'name': pages[0].link, 'title': pages[0].title, 'data': top(name)[0]}], 'active': pages[0].link,
        'meta': top_list[0]
    }
    saveViewer(request)
    return HttpResponse(template.render(context, request))


def live_view(request):
    data_list = []
    sections = Section.objects.filter(category="Live")
    for section in sections:
        data_list.append({'section_title': section.title,
                          'video_list': video("Live", request)[:20]})

    context = {'data_list': data_list, 'top_list': top_list[:45],
               'tops_of_the_week': top_video,
               'active': 'home',
               'meta': top_video[0]
               }

    saveViewer(request)
    template = loader.get_template('live.html')
    return HttpResponse(template.render(context, request))


def blog_view(request):
    tweet_list = Tweet.objects.all().order_by("-publishedAt")
    page = request.GET.get('page', 1)
    paginator = Paginator(tweet_list, 10)
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)

    context = {
        'tweets': tweets
    }
    template = loader.get_template('blog.html')
    return HttpResponse(template.render(context, request))


def b_redirect(request):
    tweetId = request.GET.get('tweetId')

    tweet = Tweet.objects.get(tweetId=tweetId)
    tweeter = Tweeter.objects.get(tweeterName=tweet.tweeter.tweeterName)

    tweet_list = Tweet.objects.filter(
        tweeter__tweeterName=tweeter.tweeterName).order_by("-publishedAt")

    page = request.GET.get('page', 1)
    paginator = Paginator(tweet_list, 10)
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)

    context = {
        'tweets': tweets,
        'meta': tweet
    }
    template = loader.get_template('blog_redirect.html')
    return HttpResponse(template.render(context, request))


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 36
    page_size_query_param = 'page_size'
    max_page_size = 1000


class VideoFilter(django_filters.FilterSet):
    class Meta:
        model = Video
        fields = ['category']

    def filter_queryset(self, queryset):
        category = self.form.cleaned_data.get('category', None)

        queryset = queryset = Video.objects.filter(Q(category=category) & (Q(status='downloaded') | Q(
            channel__channelStatus='trusted'))).order_by('-publishedAt')
        if 'modelA_id' in self.form.cleaned_data:
            pass
            # in this case will be annotated extra field to queryset
            # extra field will be based on 'modelA' instance which should be returned by serializer
        return queryset


class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = VideoFilter


class FacebookPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    tmp = datetime.today()
    start_date = tmp.replace(hour=0, minute=0, second=0)
    queryset = FacebookPost.objects.all()
    serializer_class = FacebookPostSerializer
    pagination_class = LargeResultsSetPagination
