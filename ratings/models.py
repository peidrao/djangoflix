from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django_flix.db.choices import RatingChoices

# Create your models here.

User = settings.AUTH_USER_MODEL


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
    value = models.IntegerField(null=True, blank=True, choices=RatingChoices.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self) -> str:
        return str(self.tag)