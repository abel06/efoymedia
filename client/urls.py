from django.urls import path
from client import views
from django.conf.urls import include, url
from .models import Video, Channel,  Section, Page
from rest_framework import routers, serializers, viewsets
from .views import VideoViewSet

pages = Page.objects.filter(status='published')


router = routers.DefaultRouter()
router.register(r'videos', views.VideoViewSet, basename='MyModel')
router.register(r'facebookposts', views.FacebookPostViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    # url('^videos/(?P<category>.+)/$', VideoViewSet),
    url(r'^view$', views.auto_complete, name='auto_complete'),
    url(r'^query$', views.search_youtube, name='search_youtube'),
    url(r'^download$', views.download_youtube, name='download_youtube'),
    url(r'^redirect$', views.redirect_video, name='redirect_video'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url("radio/", views.radio_view, name="radio_view"),
    url("tmp/", views.tmp_view, name="tmp_view"),
    url("live/", views.live_view, name="live_view"),
    url("blog/", views.blog_view, name="blog_view"),
    url(r'^b_redirect', views.b_redirect, name='b_redirect'),
    url(r'^listview$', views.list_view, name='listview'),
]
for page in pages:
    urlpatterns.append(
        path(page.link+'/', views.view, name=str(page.category)))
