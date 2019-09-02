from django.contrib import admin

from .models import Video, Viewer
from .models import Channel, Category, Section, Page, FacebookPost, RadioStation, Tweeter, Tweet
# ,Viewer
from embed_video.admin import AdminVideoMixin


# def make_skipped(modeladmin, request, queryset):
#     queryset.update(status='skipped')


class VideoAdmin(admin.ModelAdmin):

    def make_skipped(self, request, queryset):
        rows_updated = queryset.update(status='skipped')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(
            request, "%s successfully marked as skipped. remember to save before moving to new page" % message_bit)

    make_skipped.short_description = "Mark selected videos as skipped"
    actions = [make_skipped]
    # exclude = ('videoId',)
    channel = Channel
    list_display = ('title',
                    'view_count', 'view_count_hf', 'like_count', 'category', 'channel', 'status', 'publishedAt', 'video_tag', 'redirect_url',)

    change_list_template = (
        'admin/snippets/snippets_change_list.html')

    list_filter = ('publishedAt',
                   'status', 'category', 'channel__channelStatus', 'channel__channelCategory', 'lastModified', 'ext', 'channel__channelTitle')
    list_editable = ('status', 'category', 'channel',)
    list_per_page = 5


class ChannelAdmin(admin.ModelAdmin):

    list_display = ('channelTitle',
                    'channelStatus', 'channelCategory', 'publishedAt', 'show_firm_url', 'channelViewCount', 'channelSubscriberCount')

    list_filter = ('channelCategory', 'publishedAt',
                   'channelStatus', )
    list_editable = ('channelCategory', 'channelStatus',
                     )
    # list_per_page = 5

    change_list_template = (
        'admin/snippets/snippets_change_list.html')

    # readonly_fields = ('channelUrl',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)


class ViewerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'view_count', 'browser', 'os', 'browser_version',
                    'device', 'lastVisitAt', 'country', 'status')
    list_filter = ('lastVisitAt', 'browser', 'country', 'device')
    list_editable = ('status',)
    search_fields = ('ip',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')


class PageAdmin(admin.ModelAdmin):
    list_display = ('link', 'category', 'status')
    list_editable = ('status',)


class FacebookPostAdmin(admin.ModelAdmin):
    list_display = ("video_id", "publishedAt")
    list_filter = ("publishedAt",)


class RadioStationAdmin(admin.ModelAdmin):
    list_display = ("name", "streamUrl", )


class TweeterAdmin(admin.ModelAdmin):
    list_display = ('tweeterName', 'category', 'location',
                    'status', 'followers_count', 'statuses_count', 'show_firm_url')
    list_filter = ('category', 'status')
    list_editable = ('status',)


class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweeter', 'publishedAt', 'tweet',
                    'status', 'image', 'redirect_url')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Viewer, ViewerAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(RadioStation, RadioStationAdmin)
admin.site.register(FacebookPost, FacebookPostAdmin)
admin.site.register(Tweeter, TweeterAdmin)
admin.site.register(Tweet, TweetAdmin)
