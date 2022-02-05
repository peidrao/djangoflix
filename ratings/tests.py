import random
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.test import TestCase
from django_flix.db.choices import RatingChoices

from playlists.models import Playlist
from ratings.models import Rating


User = get_user_model()


class RatingTestCase(TestCase):
    def create_playlists(self):
        self.playlist_count = random.randint(10, 100)
        items = list()
        for i in range(0, self.playlist_count):
            items.append(Playlist(title=f'TV Show{i}'))
        Playlist.objects.bulk_create(items)
        self.playlists = Playlist.objects.all()

    def create_users(self):
        self.user_count = random.randint(10, 100)
        items = list()
        for i in range(0, self.user_count):
            items.append(User(username=f'user_{i}'))
        User.objects.bulk_create(items)
        self.users = User.objects.all()

    def create_ratings(self):
        self.rating_count = random.randint(10, 100)
        self.rating_totals = []
        items = list()
        for _ in range(0, self.rating_count):
            rating_val = random.choices(RatingChoices.choices)[0][0]
            self.rating_totals.append(rating_val)
            
            if rating_val is not None:
                self.rating_totals.append(rating_val)
                items.append(Rating(user=self.users.first(), content_object=self.playlists.last(
                ), value=rating_val))
        Rating.objects.bulk_create(items)
        self.ratings = Rating.objects.all()

    def setUp(self):
        self.create_users()
        self.create_playlists()
        self.create_ratings()

    def test_user_count(self):
        self.assertTrue(self.users.exists())
        self.assertEqual(self.users.count(), self.user_count)

    def test_playlist_count(self):
        self.assertTrue(self.playlists.exists())
        self.assertEqual(self.playlists.count(), self.playlist_count)

    def test_rating_count(self):
        self.assertTrue(self.ratings.exists())
        self.assertEqual(self.ratings.count(), self.rating_count)

    def test_rating_random_choices(self):
        values = list(Rating.objects.values_list('value', flat=True))
        self.assertTrue(len(values) > 1)

    def test_rating_agg(self):
        item_1 = Rating.objects.aggregate(average=Avg('value'))['average']
        self.assertIsNotNone(item_1)
        self.assertTrue(item_1 > 0)

    def test_rating_playlist_agg(self):
        item_1 = Playlist.objects.aggregate(
            average=Avg('ratings__value'))['average']
        self.assertIsNotNone(item_1)
        self.assertTrue(item_1 > 0)
