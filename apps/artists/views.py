from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.artists.models import Artist, Album, AlbumLike
from apps.artists.sevices import ArtistService
from apps.artists.artist_serializer import (
    ArtistSerializer, ArtistCreateSerializer, ArtistUpdateSerializer
)
from apps.artists.album_serializer import (
    AlbumSerializer, AlbumCreateSerializer, AlbumUpdateSerializer
)

from apps.users.models import Follow
from apps.users.permissions import IsOwner, IsAdmin, IsArtist, IsModerator


class ArtistListAPIView(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (AllowAny, )


class ArtistDetailAPIView(RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (AllowAny, )


class ArtistCreateAPIView(CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        user.is_artist = True
        user.save()


class ArtistUpdateAPIView(UpdateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistUpdateSerializer
    permission_classes = (IsOwner, )

    def get_object(self):
        return self.request.user.artist


class ArtistDeleteAPIView(DestroyAPIView):
    queryset = Artist.objects.all()
    permission_classes = (IsOwner | IsAdmin, )

    def get_object(self):
        if self.request.user.user_role == 'admin':
            return super().get_object()
        return self.request.user.artist

    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.is_artist = False
        user.save()


class GetTopArtistsView(ListAPIView):
    serializer_class = ArtistSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        page = self.request.GET.get('page', 1)
        return ArtistService.get_top_artists(int(page))


class SearchAristsView(ListAPIView):
    serializer_class = ArtistSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        page = self.request.GET.get('page', 1)
        return ArtistService.search_artist(query, int(page))


class CheckFollowAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'is_following': False})

        artist = get_object_or_404(Artist, pk=pk)
        is_following = Follow.objects.filter(
            follower_id=user_id,
            following=artist
        ).exists()

        return Response({'is_following': is_following})


class AlbumListAPIView(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsModerator, )


class AlbumDetailAPIView(RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (AllowAny, )


class AlbumCreateAPIView(CreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumCreateSerializer
    permission_classes = (IsArtist, )

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)


class AlbumUpdateAPIView(UpdateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return Album.objects.get(
            id=self.kwargs['pk'],
            artist=self.request.user.artist
        )


class AlbumDeleteAPIView(DestroyAPIView):
    queryset = Album.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        if self.request.user.user_role == 'admin':
            return Album.objects.get(id=self.kwargs['pk'])
        return Album.objects.get(
            id=self.kwargs['pk'],
            artist=self.request.user.artist
        )


class AlbumLikeAPIView(GenericAPIView):
    queryset = Album.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        like, created = AlbumLike.objects.get_or_create(
            album=album, user=request.user
        )

        if not created:
            like.delete()
            return Response({'status': 'unliked', 'likes': album.album_like.count()})

        return Response({'status': 'liked', 'likes': album.album_like.count()})


class AlbumLikeCheckAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'is_liked': False})

        album = get_object_or_404(Album, pk=pk)
        is_liked = AlbumLike.objects.filter(album=album, user_id=user_id).exists()
        return Response({'is_liked': is_liked})
