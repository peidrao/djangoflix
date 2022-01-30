from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save
from django.db import models
from django.utils import timezone

from categories.models import Category

from django_flix.db.choices import PlaylistTypeChoice, PublishedStateOptions
from django_flix.db.receivers import publish_state_pre_save, slugify_pre_save
from tags.models import TaggedItem

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
    parent = models.ForeignKey(
        'self', blank=True, on_delete=models.SET_NULL, null=True)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    type_video = models.CharField(max_length=3,
                                  choices=PlaylistTypeChoice.choices,
                                  default=PlaylistTypeChoice.PLAYLIST)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='playlist_category', null=True, blank=True)
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
    tags = GenericRelation(TaggedItem, related_query_name='playlist')

    objects = PlaylistManager()

    def __str__(self) -> str:
        return f'id: {self.id} - title: {self.title}'

    @property
    def is_published(self):
        return self.is_active


class TVShowProxyManager(PlaylistManager):

    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type_video=PlaylistTypeChoice.SHOW)


class TVShowProxy(Playlist):
    objects = TVShowProxyManager()

    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True

    def save(self, *args, **kwargs):
        self.type_video = PlaylistTypeChoice.SHOW
        super().save(*args, **kwargs)


class TVShowSeasonProxyManager(PlaylistManager):

    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type_video=PlaylistTypeChoice.SEASON)


class TVShowSeasonProxy(Playlist):
    objects = TVShowSeasonProxyManager()

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True

    def save(self, *args, **kwargs):
        self.type_video = PlaylistTypeChoice.SEASON
        super().save(*args, **kwargs)


class MovieProxyManager(PlaylistManager):

    def all(self):
        return self.get_queryset().filter(type_video=PlaylistTypeChoice.MOVIE)


class MovieProxy(Playlist):
    objects = MovieProxyManager()

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        proxy = True

    def save(self, *args, **kwargs):
        self.type_video = PlaylistTypeChoice.MOVIE
        super().save(*args, **kwargs)


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
