from django.urls import path

from apps.artists.views import (ArtistListAPIView, ArtistDetailAPIView, ArtistCreateAPIView,
ArtistDeleteAPIView, ArtistUpdateAPIView, SearchAristsView, GetTopArtistsView)

app_name = 'artists'

urlpatterns = [
    path('', ArtistListAPIView.as_view(), name='artist_list'),
    path('<int:pk>/', ArtistDetailAPIView.as_view(), name='artist_detail'),
    path('create/', ArtistCreateAPIView.as_view(), name='artist_create'),
    path('update/', ArtistUpdateAPIView.as_view(), name='artist_update'),
    path('<int:pk>/delete/', ArtistDeleteAPIView.as_view(), name='artist_delete'),
    path('top/', GetTopArtistsView.as_view(), name='top_artists'),
    path('search/', SearchAristsView.as_view(), name='search_artists'),
]