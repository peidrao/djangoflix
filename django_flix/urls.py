
from django.contrib import admin
from django.urls import path, re_path

from playlists.views import (
    FeaturedPlaylistListView, 
    MovieListView, 
    PlaylistDetailView,
    TVShowDetailView,
    TVShowListView,
    MovieDetailView,
    TVShowSeasonDetailView
)



urlpatterns = [
    re_path(r'my-detail/(?P<id>\d+)/$', FeaturedPlaylistListView.as_view()),
    path('', FeaturedPlaylistListView.as_view()),
    path('admin/', admin.site.urls),
    path('movies/', MovieListView.as_view()),
    path('movies/<slug:slug>', MovieDetailView.as_view()),
    path('playlist/<slug:slug>', PlaylistDetailView.as_view()),
    path('media/<int:id>', FeaturedPlaylistListView.as_view()),
    path('shows/<slug:showSlug>/seasons/<slug:seasonSlug>',
         TVShowSeasonDetailView.as_view()),
    path('shows/<slug:slug>/seasons/', TVShowSeasonDetailView.as_view()),
    path('shows/<slug:slug>/', TVShowDetailView.as_view()),
    path('shows/', TVShowListView.as_view()),

]
