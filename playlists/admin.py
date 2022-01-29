from django.contrib import admin

from .models import Playlist


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'state']
    search_fields = ['title', 'state']
    list_filter = ['is_active', 'state']
    readonly_fields = ['id', 'is_published', 'published_timestamp']

    class Meta:
        model = Playlist


admin.site.register(Playlist, PlaylistAdmin)