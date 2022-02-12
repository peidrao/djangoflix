from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify


from django_flix.db.choices import PublishedStateOptions
from .models import Playlist, MovieProxy
from videos.models import Video


class PlaylistModelTestCase(TestCase):

    def create_show_with_seasons(self):
        self.the_office = Playlist.objects.create(title='The Office')
        Playlist.objects.create(title='The Office - Season 1',
                                parent=self.the_office,
                                order=1)
        Playlist.objects.create(title='The Office - Season 2',
                                parent=self.the_office,
                                order=2)
        Playlist.objects.create(title='The Office - Season 3',
                                parent=self.the_office,
                                order=3)

    def create_video(self):
        self.video1 = Video.objects.create(title='Video #1', video_id='abc123')
        self.video2 = Video.objects.create(title='Video #2', video_id='abc456')
        self.video3 = Video.objects.create(title='Video #3', video_id='abc789')

    def setUp(self):
        self.create_video()
        self.create_show_with_seasons()
        self.playlist1 = Playlist.objects.create(title='Playlist #1',
                                                 video=self.video1)
        self.playlist2 = Playlist.objects.create(
            title='Playlist #2',
            video=self.video1,
            state=PublishedStateOptions.PUBLISHED)
        self.playlist2.videos.add(self.video1, self.video2, self.video3)
        self.playlist2.save()

    def test_show_has_seasons(self):
        seasons = self.the_office.playlist_set.all()
        self.assertTrue(seasons.exists())

    def test_video_playlist(self):
        qs = self.video1.featured_playlist.all()
        self.assertEqual(qs.count(), 2)

    def test_playlist_video_items(self):
        qs = self.playlist2.videos.all()
        self.assertEqual(qs.count(), 3)

    def test_video_playlist_ids_property(self):
        ids = self.playlist1.video.get_playlists_ids()
        actual_ids = list(
            Playlist.objects.filter(video=self.video1).values_list('id',
                                                                   flat=True))
        self.assertEqual(ids, actual_ids)

    def test_valid_title(self):
        title = 'Playlist #1'
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 6)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(), 5)

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


class MovieProxyTestCase(TestCase):
    def create_videos(self):
        video_a = Video.objects.create(title='My title', video_id='abc123')
        video_b = Video.objects.create(title='My title', video_id='abc1233')
        video_c = Video.objects.create(title='My title', video_id='abc1234')
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        self.video_qs = Video.objects.all()

    def setUp(self):
        self.create_videos()
        self.movie_title = 'This is my title'
        self.movie_a = MovieProxy.objects.create(title=self.movie_title, video=self.video_a)
        movie_b = MovieProxy.objects.create(title='This is my title', state=PublishedStateOptions.PUBLISHED, video=self.video_a)
        self.published_item_count = 1
        movie_b.videos.set(self.video_qs)
        movie_b.save()
        self.movie_b = movie_b

    def test_movie_video(self):
        self.assertEqual(self.movie_a.video, self.video_a)

    def test_movie_clip_items(self):
        count = self.movie_b.videos.all().count()
        self.assertEqual(count, 3)
    
    def test_valid_title(self):
        title= self.movie_title
        qs = MovieProxy.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_draft_case(self):
        qs = MovieProxy.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_manager(self):
        published_qs = MovieProxy.objects.all().published()
        published_qs_2 = MovieProxy.objects.published()
        self.assertEqual(published_qs.count(), published_qs_2.count())