from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'id: {self.id} - title: {self.title}'


class VideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'