from enum import unique
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # CONSTANT = DB_VALUE, USER_DISPLAY_VA
        PUBLISHED = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Publish'
        # PRIVATE = 'PR', 'Private'

    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'id: {self.id} - title: {self.title}'

    @property
    def is_published(self):
        return self.is_active

    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISHED and self.published_timestamp is None:
            self.published_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.published_timestamp = None
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'
