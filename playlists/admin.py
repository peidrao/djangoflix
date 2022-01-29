from django.contrib import admin

from .models import Playlist, PlaylistItem


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


admin.site.register(Playlist, PlaylistAdmin)
