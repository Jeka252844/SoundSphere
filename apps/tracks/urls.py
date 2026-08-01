from django.urls import path

from apps.tracks.views import (
    TracksListAPIView, TrackDetailAPIView, SearchTracksView, TrackCreateAPIView,
    TrackUpdateAPIView, TrackDeleteAPIView, TopTracksWeeklyView, GenreListAPIView, TrackLikeAPIView,
    TrackLikeCheckAPIView
)

app_name = 'tracks'

urlpatterns = [
    path('list/', TracksListAPIView.as_view(), name='track_list'),
    path('<int:pk>/', TrackDetailAPIView.as_view(), name='track_detail'),
    path('create/', TrackCreateAPIView.as_view(), name='track_create'),
    path('<int:pk>/update/', TrackUpdateAPIView.as_view(), name="track_update"),
    path('<int:pk>/delete/', TrackDeleteAPIView.as_view(), name='track_delete'),
    path('top/', TopTracksWeeklyView.as_view(), name='top_tracks'),
    path('search/', SearchTracksView.as_view(), name='search_tracks'),
    path('<int:pk>/like/', TrackLikeAPIView.as_view(), name='track_like'),
    path('<int:pk>/like/check/', TrackLikeCheckAPIView.as_view(), name='track_like_check'),

    path('genre/list/', GenreListAPIView.as_view(), name='genre_list'),
]
