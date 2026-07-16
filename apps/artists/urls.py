from django.urls import path

from apps.artists.views import (ArtistListAPIView, ArtistDetailAPIView, ArtistCreateAPIView,
ArtistDeleteAPIView, ArtistUpdateAPIView, SearchAristsView, GetTopArtistsView,
AlbumCreateAPIView, AlbumDetailAPIView, AlbumDeleteAPIView, AlbumUpdateAPIView, AlbumListAPIView)


app_name = 'artists'

urlpatterns = [
    # artist
    path('', ArtistListAPIView.as_view(), name='artist_list'),
    path('<int:pk>/', ArtistDetailAPIView.as_view(), name='artist_detail'),
    path('create/', ArtistCreateAPIView.as_view(), name='artist_create'),
    path('update/', ArtistUpdateAPIView.as_view(), name='artist_update'),
    path('<int:pk>/delete/', ArtistDeleteAPIView.as_view(), name='artist_delete'),
    path('top/', GetTopArtistsView.as_view(), name='top_artists'),
    path('search/', SearchAristsView.as_view(), name='search_artists'),

    # album
    path('album/', AlbumListAPIView.as_view(), name="album_list"),
    path('album/<int:pk>/', AlbumDetailAPIView.as_view(), name="album_detail"),
    path('album/create/', AlbumCreateAPIView.as_view(), name='album_create'),
    path('album/<int:pk>/update/', AlbumUpdateAPIView.as_view(), name='album_update'),
    path('album/<int:pk>/delete/', AlbumDeleteAPIView.as_view(), name='album_delete'),
]