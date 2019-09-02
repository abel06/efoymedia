from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Video, Channel, Viewer, Section, Page, Category, FacebookPost


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    channelCategory = CategorySerializer()

    class Meta:
        model = Channel
        fields = ('channelTitle', 'channelCategory')


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    channel = ChannelSerializer()

    class Meta:
        model = Video
        fields = ('videoId',  'title',  'channel', 'publishedAt', 'thumbnailsLow', 'thumbnailsHigh', 'thumbnailsMedium', 'url',  'description',
                  'ext',  'view_count', 'like_count', 'dislike_count', 'video')
        depth = 1


class FacebookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPost
        fields = '__all__'
