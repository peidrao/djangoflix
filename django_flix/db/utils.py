import random
import string
from django.utils.text import slugify

from playlists.models import Playlist


def get_random_string(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join([random.choice(chars) for _ in range(size)])

def get_unique_slug(instance, new_slug=None):
    title = instance.title
    rand_str = get_random_string()
    if new_slug is None:
        slug = slugify(title) + rand_str
    else:
        slug = new_slug
    
    qs = Playlist.objects.filter(slug=slug)
    if qs.exists():
        new_slug = slugify(title) + rand_str
        return get_unique_slug(instance, new_slug=new_slug)
    return slug
