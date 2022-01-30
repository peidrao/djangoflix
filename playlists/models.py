from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django_flix.db.choices import PublishedStateOptions
from django_flix.db.receivers import publish_state_pre_save, slugify_pre_save

from videos.models import Video


class PlaylistQuerySet(models.QuerySet):

    def published(self):
        now = timezone.now()
        return self.filter(state=PublishedStateOptions.PUBLISHED,
                           published_timestamp__lte=now)


class PlaylistManager(models.Manager):

    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    video = models.ForeignKey(Video,
                              null=True,
                              related_name='featured_playlist',
                              on_delete=models.SET_NULL)
    videos = models.ManyToManyField(Video,
                                    related_name='playlist_item',
                                    blank=True,
                                    through='PlaylistItem')
    state = models.CharField(max_length=2,
                             choices=PublishedStateOptions.choices,
                             default=PublishedStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(auto_now_add=False,
                                               auto_now=False,
                                               blank=True,
                                               null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PlaylistManager()

    def __str__(self) -> str:
        return f'id: {self.id} - title: {self.title}'

    @property
    def is_published(self):
        return self.is_active


class TVShowProxyManager(PlaylistManager):

    def all(self):
        return self.get_queryset().filter(parent__isnull=True)


class TVShowProxy(Playlist):
    objects = TVShowProxyManager()

    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True


class TVShowSeasonProxyManager(PlaylistManager):

    def all(self):
        return self.get_queryset().filter(parent__isnull=False)


class TVShowSeasonProxy(Playlist):
    objects = TVShowSeasonProxyManager()

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self) -> str:
        return f'Playlist: {self.playlist.title}'


pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)
