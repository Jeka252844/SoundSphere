from rest_framework.generics import (ListAPIView, RetrieveAPIView, 
CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import AllowAny

from apps.tracks.models import Track, Genre
from apps.tracks.services import TrackService
from apps.users.permissions import IsArtist, IsModerator, IsAdmin, IsOwner
from apps.tracks.track_serializer import TrackSerializer, TrackCreateSerializer, TrackUpdateSerializer

class TrackDetailAPIView(RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )

class TrackCreateAPIView(CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackCreateSerializer
    permission_classes = (IsArtist, )

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)

class TrackUpdateAPIView(UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackUpdateSerializer
    permission_classes = (IsArtist, )

class TrackDeleteAPIView(DestroyAPIView):
    queryset = Track.objects.all()
    permission_classes = (IsArtist | IsModerator, )

class TopGenreTracksViews(ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        genre_name = self.request.GET.get('genre_name')
        page = self.request.GET.get('page', 1)
        if genre_name:
            return TrackService.get_top_by_genre(genre_name, int(page))
        return TrackService.get_top_tracks(int(page))
    
class GetTracksView(ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        genre_name = self.request.GET.get('genre_name')
        artist_name = self.request.GET.get('artist_name')
        page = self.request.GET.get('page', 1)
        return TrackService.search_track(query, genre_name, artist_name, int(page))