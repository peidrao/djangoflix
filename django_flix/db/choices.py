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


class RatingChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = 'Unknown'
