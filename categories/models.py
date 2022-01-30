from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_save

from django_flix.db.receivers import slugify_pre_save
from tags.models import TaggedItem
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = GenericRelation(TaggedItem, related_query_name='category')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return f'{self.title}'


pre_save.connect(slugify_pre_save, sender=Category)
