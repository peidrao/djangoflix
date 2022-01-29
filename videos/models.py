from django.db import models
from django.utils import timezone

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
    video_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    created_at = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self) -> str:
        return f'id: {self.id} - title: {self.title}'

    @property
    def is_published(self):
        return self.is_active
    
    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISHED and self.created_at is None:
            print('save as timestamp for published')
            self.created_at = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.created_at = None
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
