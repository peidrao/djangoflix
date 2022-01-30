import imp
from django.db import models


class PublishedStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    PUBLISHED = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN', 'Publish'
    # PRIVATE = 'PR', 'Private'


class PlaylistTypeChoice(models.TextChoices):
    MOVIE = 'MOV', 'Movie'
    SHOW = 'TVS', 'TV Show'
    SEASON = 'SEA', 'Season'
    PLAYLIST = 'PLY', 'Playlist'