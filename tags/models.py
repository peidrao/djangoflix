from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django_flix.db.receivers import slugify_pre_save


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self) -> str:
        return str(self.tag)

    def get_related_object(self):
        Klass = self.content_type.model_class()
        return Klass.objects.get(id=self.object_id)

# pre_save.connect(slugify_pre_save, sender=TaggedItem)
