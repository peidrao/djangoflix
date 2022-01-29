from django.test import TestCase
from django.utils import timezone

from .models import Video, PublishedStateOptions


class VideoModelTestCase(TestCase):
    def setUp(self):
        self.video1 = Video.objects.create(title='This is my video!', video_id='123')
        self.video2 =Video.objects.create(title='This is life!',
                             state=PublishedStateOptions.PUBLISHED, video_id='456')
    def test_slug_field(self):
        self.assertEqual(self.video1.slug, 'this-is-my-video')
        self.assertEqual(self.video2.slug, 'this-is-life')

    def test_valid_title(self):
        title = 'This is my video!'
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_published_case(self):
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=PublishedStateOptions.PUBLISHED, created_at__lte=now)
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = Video.objects.all().published()
        published_qs2 = Video.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertTrue(published_qs2.exists())
        self.assertEqual(published_qs.count(), published_qs2.count())