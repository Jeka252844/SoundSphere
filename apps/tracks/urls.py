from django.urls import path

from apps.tracks.views import (TrackListAPIView, TrackDetailAPIView, 
    TrackCreateAPIView, TrackUpdateAPIView, TrackDeleteAPIView)

app_name='tracks'

urlpatterns = [
    path('', TrackListAPIView.as_view(), name='track_list'),
    path('<int:pk>/', TrackDetailAPIView.as_view(), name='track_detail'),
    path('create/', TrackCreateAPIView.as_view(), name='track_create'),
    path('<int:pk>/update/', TrackUpdateAPIView.as_view(), name="track_update"),
    path('<int:pk>/delete/', TrackDeleteAPIView.as_view(), name='track_delete')
]
