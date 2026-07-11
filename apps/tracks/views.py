from rest_framework.generics import (ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import AllowAny

from apps.tracks.models import Track, Genre
from apps.users.permissions import IsArtist, IsModerator, IsAdmin, IsOwner
from apps.tracks.track_serializer import TrackSerializer, TrackCreateSerializer, TrackUpdateSerializer

class TrackListAPIView(ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )

class TrackDetailAPIView(RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )

class TrackCreateAPIView(CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackCreateSerializer
    permission_classes = (IsArtist, )

class TrackUpdateAPIView(UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackUpdateSerializer
    permission_classes = (AllowAny, )

class TrackDeleteAPIView(DestroyAPIView):
    queryset = Track.objects.all()
    permission_classes = (AllowAny, )