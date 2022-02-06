from django.shortcuts import render
from django.views import generic

from .models import MovieProxy, Playlist, TVShowProxy
# Create your views here.


class TitleMixin():
    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.title
        return context
    


class MovieListView(TitleMixin, generic.ListView):
    template_name = 'playlist_list.html'
    queryset = MovieProxy.objects.all()
    title = 'Movies'


class TVShowListView(TitleMixin, generic.ListView):
    template_name = 'tvshow_list.html'
    queryset = TVShowProxy.objects.all()
    title = 'TV Shows'


class FeaturedPlaylistListView(TitleMixin, generic.ListView):
    template_name = 'tvshow_list.html'
    queryset = Playlist.objects.featured_playlist()
    title = 'Featured'
