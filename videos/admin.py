from django.contrib import admin

from .models import Video, VideoPublishedProxy, VideoAllProxy


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'is_published']
    search_fields = ['title']
    list_filter = ['is_active']
    readonly_fields = ['id', 'is_published', 'timestamp']

    class Meta:
        model = VideoAllProxy


class VideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(is_active=True)


admin.site.register(VideoAllProxy, VideoAllAdmin)
admin.site.register(VideoPublishedProxy, VideoProxyAdmin)
