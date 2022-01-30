from django.test import TestCase

from .models import Category


class CategoryTestCase(TestCase):

    def setUp(self):
        self.cat_a = Category.objects.create(title='Action')
        self.cat_b = Category.objects.create(title='Comedy', is_active=False)

    def test_is_active(self):
        self.assertTrue(self.cat_a.is_active)

    def test_not_is_active(self):
        self.assertFalse(self.cat_b.is_active)
