from django.contrib import admin

from django_flix.db.choices import PlaylistTypeChoice
from tags.admin import TaggedItemInline
from .models import MovieProxy, Playlist, PlaylistItem, TVShowProxy, TVShowSeasonProxy


class MovideProxyAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'description', 'state', 'video', 'slug', 'category']

    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()


class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SeasonEpisodeInline]
    list_display = ['title', 'parent']

    class Meta:
        model = TVShowSeasonProxy

    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()


class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 2
    fields = ['order', 'title', 'state']


class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TVShowSeasonProxyInline, TaggedItemInline]
    fields = ['title', 'description', 'state', 'video', 'slug', 'category']

    class Meta:
        model = TVShowProxy

    def get_queryset(self, request):
        return TVShowProxy.objects.all()


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]

    list_display = ['title', 'is_published', 'state']
    search_fields = ['title', 'state']
    list_filter = ['is_active', 'state']
    readonly_fields = ['id', 'is_published', 'published_timestamp']

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type_video=PlaylistTypeChoice.PLAYLIST)


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MovieProxy, MovideProxyAdmin)
admin.site.register(TVShowProxy, TVShowProxyAdmin)
admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)
