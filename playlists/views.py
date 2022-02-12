from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .models import MovieProxy, Playlist, TVShowProxy, TVShowSeasonProxy
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


class PlaylistDetailView(TitleMixin, generic.DetailView):
    template_name = 'playlist/playlist_detail.html'
    queryset = Playlist.objects.all()
    title = 'Playlist'


class MovieDetailView(TitleMixin, generic.DetailView):
    template_name = 'playlist/movie_detail.html'
    queryset = MovieProxy.objects.all()
    title = 'Movies'


class TVShowDetailView(TitleMixin, generic.DetailView):
    template_name = 'playlist/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()
    title = 'Movies'


class TVShowSeasonDetailView(TitleMixin, generic.DetailView):
    template_name = 'playlist/tvshow_seasons_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        show_slug = self.kwargs.get('showSlug')
        season_slug = self.kwargs.get('seasonSlug')
        qs = self.get_queryset().filter(
            parent__slug__iexact=show_slug, slug__iexact=season_slug)
        
        if not qs.count() == 1:
            raise Http404
        return qs.first()


class TVShowListView(TitleMixin, generic.ListView):
    template_name = 'tvshow_list.html'
    queryset = TVShowProxy.objects.all()
    title = 'TV Shows'


class FeaturedPlaylistListView(TitleMixin, generic.ListView):
    template_name = 'tvshow_list.html'
    queryset = Playlist.objects.featured_playlist()
    title = 'Featured'
