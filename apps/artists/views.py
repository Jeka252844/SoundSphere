from rest_framework.generics import (ListAPIView, RetrieveAPIView, 
CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.artists.models import Artist, Album
from apps.users.models import User
from apps.artists.artist_serializer import (ArtistSerializer, 
ArtistCreateSerializer, ArtistUpdateSerializer)
from apps.users.permissions import IsOwner, IsAdmin

class ArtistListAPIView(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class =  ArtistSerializer
    permission_classes = (IsAdmin, )

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
        user = self.request.user
        return User.objects.get(id = user.id)

class ArtistDeleteAPIView(DestroyAPIView):
    queryset = Artist.objects.all()
    permission_classes = (IsOwner | IsAdmin, )