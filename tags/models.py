from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType

from django_flix.db.receivers import slugify_pre_save


class TaggedItem(models.Model):
    tag = models.SlugField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.tag)


pre_save.connect(slugify_pre_save, sender=TaggedItem)
