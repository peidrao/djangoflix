
from django.contrib import admin
from django.urls import path, re_path

from playlists.views import FeaturedPlaylistListView, MovieListView, TVShowListView

urlpatterns = [
    re_path(r'my-detail/(?P<id>\d+)/$', FeaturedPlaylistListView.as_view()),
    path('', FeaturedPlaylistListView.as_view()),
    path('admin/', admin.site.urls),
    path('movies/', MovieListView.as_view()),
    path('movies/<slug:slug>', MovieListView.as_view()),
    path('media/<int:id>', FeaturedPlaylistListView.as_view()),
    path('shows/<slug:showSlug>/seasons/<slug:seasonSlug>', TVShowListView.as_view()),
    path('shows/<slug:slug>/seasons/', TVShowListView.as_view()),
    path('shows/<slug:slug>/', TVShowListView.as_view()),
    path('shows/', TVShowListView.as_view()),

]
