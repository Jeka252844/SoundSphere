from rest_framework.generics import (ListAPIView, RetrieveAPIView, 
CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.artists.models import Artist, Album
from apps.artists.sevices import ArtistService
from apps.artists.artist_serializer import (ArtistSerializer, 
ArtistCreateSerializer, ArtistUpdateSerializer)
from apps.artists.album_serializer import (AlbumSerializer,
AlbumCreateSerializer, AlbumUpdateSerializer)

from apps.users.models import User
from apps.users.permissions import IsOwner, IsAdmin, IsArtist, IsModerator

class ArtistListAPIView(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class =  ArtistSerializer
    permission_classes = (IsModerator, )

class ArtistDetailAPIView(RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (AllowAny, )

class ArtistCreateAPIView(CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

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
        serializer.save(artist = self.request.user.artist)

class AlbumUpdateAPIView(UpdateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return Album.objects.get(
            id = self.kwargs['pk'],
            artist = self.request.user.artist
        )
    
class AlbumDeleteAPIView(DestroyAPIView):
    queryset = Album.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        if self.request.user.user_role == 'admin':
            return Album.objects.get(id = self.kwargs['pk'])
        return Album.objects.get(
            id = self.kwargs['pk'],
            artist = self.request.user.artist
        )