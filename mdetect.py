from django.db import models
from django.contrib import admin
from django.utils.html import format_html
import datetime
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator
import re

STATUS = (
    ('pending', 'PENDING'),
    ('downloaded', 'DOWNLOADED'),
    ('uploaded', 'UPLOADED'),
    ('skipped', 'SKIPPED'),

)
STAT = (
    ('published', "PUBLISHED"),
    ('unpublished', 'UNPUBLISHED')
)

PUBLISHED = (('published', 'published'), ('unpublished', 'unpublished'))

CATERGORIES = (
    ('unset', 'UNSET'),
    ('music', 'MUSIC'),
    ('movie', 'MOVIE'),
    ('tv_series', 'TV_SERIES'),
    ('song', 'SONG'),
)

CHANNEL_CATEGORIES = (
    ('unset', 'UNSET'),
    ('trusted', 'TRUSTED'),
    ('untrusted', 'UNTRUSTED')
)


class Category(models.Model):
    # categoryId = models.CharField(max_length=200, primary_key=True)
    category = models.CharField(
        max_length=20, default='Unset', primary_key=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Channel(models.Model):
    channelId = models.CharField(max_length=200, primary_key=True)
    channelTitle = models.CharField(max_length=200)
    channelStatus = models.CharField(
        max_length=10, choices=CHANNEL_CATEGORIES, default='unset')
    channelCategory = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=Category)
    channelUrl = models.URLField(max_length=250)
    channelViewCount = models.IntegerField(null=True, blank=True)
    channelCommentCount = models.IntegerField(null=True, blank=True)
    channelSubscriberCount = models.IntegerField(null=True, blank=True)
    channelVideoCount = models.IntegerField(null=True, blank=True)

    publishedAt = models.DateTimeField(
        'publishedAt', null=True)

    class Meta:
        verbose_name_plural = 'Channels'

    def __str__(self):
        return self.channelTitle

    def show_firm_url(self):
        return format_html('<a href="%s">%s</a>' % (self.channelUrl, self.channelUrl))
    show_firm_url.allow_tags = True


class Video(models.Model):
    now = timezone.now()
    videoId = models.CharField(max_length=200, primary_key=True)
    # channelId = models.CharField(max_length=200)
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, default=Channel)

    title = models.CharField(max_length=200)
    channelTitle = models.CharField(max_length=200)
    publishedAt = models.DateTimeField(blank=True, null=True)
    lastModified = models.DateTimeField(blank=True, null=True)

    thumbnailsLow = models.URLField(max_length=250, blank=True, null=True)
    thumbnailsHigh = models.URLField(max_length=250, blank=True, null=True)
    thumbnailsMedium = models.URLField(max_length=250, blank=True, null=True)
    url = models.URLField(max_length=250)
    license = models.CharField(max_length=200, null=True, blank=True)
    creator = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=Category)

    subtitles = models.CharField(max_length=200, null=True, blank=True)
    artist = models.CharField(max_length=200, null=True, blank=True)
    track = models.CharField(max_length=200, null=True, blank=True)
    width = models.IntegerField()
    height = models.IntegerField()
    resolution = models.CharField(max_length=200, null=True, blank=True)
    ext = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, blank=True)
    view_count = models.IntegerField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    dislike_count = models.IntegerField(default=0, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    video = models.URLField(max_length=300)

    def video_tag(self):
        # return format_html('<img src="{}" style="width:100px;height:100px;" />'.format(self.thumbnails))
        return format_html('<iframe src="{}"   type="text/html" width="300" height="150"  frameborder="0" allowfullscreen="allowfullscreen"></iframe>'.format(self.video))

    def image_tag(self):
        return format_html('<img src="{}" style="width:100px;height:100px;" />'.format(self.thumbnails))

    def category_tag(self):
        # return format_html('<img src="{}" style="width:100px;height:100px;" />'.format(self.thumbnails))
        return self.channel.channelCategory
    def redirect_url(self):
        return "https://www.efoymedia.com/redirect?videoId="+self.videoId
    video_tag.short_description = 'Video'
    video_tag.allow_tags = True
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    category_tag.short_description = 'Category'
    category_tag.allow_tags = True

    class Meta:
        verbose_name_plural = 'Videos'


class Viewer(models.Model):
    user = models.CharField(max_length=200, null=True, blank=True)
    ip = models.CharField(max_length=200, null=True, blank=True)
    lastVisitAt = models.DateTimeField(blank=True, null=True)
    browser = models.CharField(max_length=200, null=True, blank=True)
    browser_version = models.CharField(max_length=5, null=True, blank=True)
    os = models.CharField(max_length=20, null=True, blank=True)
    os_version = models.CharField(max_length=20, null=True, blank=True)
    device = models.CharField(max_length=20, null=True, blank=True)
    view_count = models.IntegerField(blank=True, default=0, null=True)
    continent = models.CharField(max_length=20,  blank=True)
    country = models.CharField(max_length=200,  blank=True)
    city = models.CharField(max_length=200,  blank=True)
    timezone = models.CharField(max_length=200,  blank=True)

    class Meta:
        verbose_name_plural = 'Viewers'


class Section(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=Category)

    class Meta:
        verbose_name_plural = 'Sections'


alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Page(models.Model):
    link = models.CharField(
        max_length=20, primary_key=True, validators=[alphanumeric])

    title = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=Category)

    status = models.CharField(
        max_length=12, choices=PUBLISHED, default='unpublished')

    class Meta:
        verbose_name_plural = 'Pages'


# class PostTag(models.Model):
#     postTag = models.TextField()
#     publishedAt = models.DateTimeField(blank=True, null=True)


class FacebookPost(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, default=Video)
    PostTag = models.TextField(blank=True)

    publishedAt = models.DateTimeField(blank=True, null=True)
    account = models.CharField(max_length=200, null=True, blank=True)

class RadioStation(models.Model):
    stationId = models.CharField(max_length=200, primary_key=True)
    name=models.CharField(max_length=200, null=True, blank=True)
    streamUrl= models.URLField(max_length=250)
    desc=models.TextField(blank=True)
    status=models.CharField(
        max_length=10, choices=STAT, default='unpublished')

class Tweeter(models.Model):
    tweeterName = models.CharField(max_length=200, primary_key=True)
    status = models.CharField(
        max_length=10, choices=CHANNEL_CATEGORIES, default='unset')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=Category)
    url = models.URLField(max_length=250)
    followers_count = models.IntegerField(null=True, blank=True)
    statuses_count = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    publishedAt = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    image = models.URLField(max_length=250)

    def __str__(self):
        return self.tweeterName

    def show_firm_url(self):
        return format_html('<a href="%s">%s</a>' % (self.url, self.url))
    show_firm_url.allow_tags = True


class Tweet(models.Model):
    tweetId = models.CharField(max_length=200, primary_key=True)
    tweet = models.TextField(null=True, blank=True)
    tweeter = models.ForeignKey(
        Tweeter, on_delete=models.CASCADE, default=Tweeter)
    publishedAt = models.DateTimeField(blank=True, null=True)
    image = models.URLField(max_length=250, blank=True,)
    status = models.CharField(
        max_length=12, choices=PUBLISHED, default='unpublished')

    def fullTweet(self):
        try:
            url = re.search(
                "(?P<url>https?://[^\s]+)", self.tweet).group("url")
            self.tweet = re.sub(url, '<a href="%s">%s</a>' %
                                (url, url), self.tweet)
            return self.tweet
        except:
            return self.tweet
    def redirect_url(self):
        return "https://www.efoymedia.com/b_redirect?tweetId="+self.tweetId