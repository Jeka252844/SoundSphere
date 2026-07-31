from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from apps.tracks.models import Track, Genre, TrackLike
from apps.tracks.services import TrackService
from apps.users.permissions import IsArtist, IsModerator, IsAdmin, IsOwner
from apps.tracks.track_serializer import TrackSerializer, TrackCreateSerializer, TrackUpdateSerializer, GenreSerializer


class TracksListAPIView(ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (IsModerator, )


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
    permission_classes = (IsOwner, )


class TrackDeleteAPIView(DestroyAPIView):
    queryset = Track.objects.all()
    permission_classes = (IsOwner | IsAdmin, )


class TopTracksWeeklyView(ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return TrackService.get_top_tracks_weekly()


class SearchTracksView(ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        genre_name = self.request.GET.get('genre_name')
        artist_name = self.request.GET.get('artist_name')
        page = self.request.GET.get('page', 1)
        return TrackService.search_track(query, genre_name, artist_name, int(page))


class TrackLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        track = get_object_or_404(Track, pk=pk)
        like, created = TrackLike.objects.get_or_create(
            track=track, user=request.user
        )
        if not created:
            like.delete()
            return Response({
                'status': 'unliked',
                'likes': track.track_likes.count()
            })
        return Response({
            'status': 'liked',
            'likes': track.track_likes.count()
        })


class TrackLikeCheckAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'is_liked': False})
        track = get_object_or_404(Track, pk=pk)
        is_liked = TrackLike.objects.filter(track=track, user_id=user_id).exists()
        return Response({'is_liked': is_liked})


class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny, )
