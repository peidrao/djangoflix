
from django.contrib import admin
from django.urls import path

from playlists.views import FeaturedPlaylistListView, MovieListView, TVShowListView

urlpatterns = [
    path('', FeaturedPlaylistListView.as_view()),
    path('admin/', admin.site.urls),
    path('movies/', MovieListView.as_view()),
    path('shows/', TVShowListView.as_view()),
]
