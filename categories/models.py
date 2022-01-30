from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'