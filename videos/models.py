
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify


class PublishedStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    PUBLISHED = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN', 'Publish'
    # PRIVATE = 'PR', 'Private'


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=PublishedStateOptions.PUBLISHED, published_timestamp__lte=now)


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2, choices=PublishedStateOptions.choices, default=PublishedStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VideoManager()

    def __str__(self) -> str:
        return f'id: {self.id} - title: {self.title}'

    @property
    def is_published(self):
        return self.is_active


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


def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == PublishedStateOptions.PUBLISHED
    is_draft = instance.state == PublishedStateOptions.DRAFT
    if is_publish and instance.published_timestamp is None:
        instance.published_timestamp = timezone.now()
    elif is_draft:
        instance.published_timestamp = None


def slugify_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)


pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)
