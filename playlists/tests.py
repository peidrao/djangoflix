from django.test import TestCase
from django.utils import timezone

from .models import Playlist, PublishedStateOptions
from videos.models import Video


class PlaylistModelTestCase(TestCase):
    def create_video(self):
        self.video1 = Video.objects.create(title='Video #1', video_id='abc123')
        self.video2 = Video.objects.create(title='Video #2', video_id='abc456')
        self.video3 = Video.objects.create(title='Video #3', video_id='abc789')

    def setUp(self):
        self.create_video()

        self.playlist1 = Playlist.objects.create(
            title='Playlist #1', video=self.video1)
        self.playlist2 = Playlist.objects.create(title='Playlist #2', video=self.video1,
                                                 state=PublishedStateOptions.PUBLISHED)
        self.playlist2.videos.add(self.video1, self.video2, self.video3)
        self.playlist2.save()

    def test_video_playlist(self):
        qs = self.video1.featured_playlist.all()
        self.assertEqual(qs.count(), 2)

    def test_playlist_video_items(self):
        qs = self.playlist2.videos.all()
        self.assertEqual(qs.count(), 3)

    def test_slug_field(self):
        self.assertEqual(self.playlist1.slug, 'playlist-1')
        self.assertEqual(self.playlist2.slug, 'playlist-2')

    def test_video_playlist_ids_property(self):
        ids = self.playlist1.video.get_playlists_ids()
        actual_ids = list(Playlist.objects.filter(
            video=self.video1).values_list('id', flat=True))
        self.assertEqual(ids, actual_ids)

    def test_valid_title(self):
        title = 'Playlist #1'
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_published_case(self):
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishedStateOptions.PUBLISHED, created_at__lte=now)
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = Playlist.objects.all().published()
        published_qs2 = Playlist.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertTrue(published_qs2.exists())
        self.assertEqual(published_qs.count(), published_qs2.count())
