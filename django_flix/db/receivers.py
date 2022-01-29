from django.utils import timezone
from django.utils.text import slugify

from .choices import PublishedStateOptions


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
