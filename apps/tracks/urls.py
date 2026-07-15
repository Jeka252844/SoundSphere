from django.urls import path

from apps.tracks.views import (TrackDetailAPIView, SearchTracksView, TrackCreateAPIView
    , TrackUpdateAPIView, TrackDeleteAPIView, TopGenreTracksViews)

app_name='tracks'

urlpatterns = [
    path('<int:pk>/', TrackDetailAPIView.as_view(), name='track_detail'),
    path('create/', TrackCreateAPIView.as_view(), name='track_create'),
    path('<int:pk>/update/', TrackUpdateAPIView.as_view(), name="track_update"),
    path('<int:pk>/delete/', TrackDeleteAPIView.as_view(), name='track_delete'),
    path('top/', TopGenreTracksViews.as_view(), name='top_tracks'),
    path('search/', SearchTracksView.as_view(), name='search_tracks')
]
