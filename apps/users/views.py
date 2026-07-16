from rest_framework.generics import (ListAPIView, CreateAPIView, GenericAPIView, 
    UpdateAPIView, DestroyAPIView, RetrieveAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from apps.users.models import User, Follow, PlayList, PlayListTrack
from apps.artists.models import Artist
from apps.tracks.models import Track
from apps.users.permissions import IsAdmin, IsModerator, IsOwner

from apps.users.user_serializer import (UserSerializer, UserCreateSerializer,
 UserUpdateSerializer, UserPasswordSerializer)
from apps.users.playlist_serializer import (PlayListSerializer,
 PlayListCreateSerializer, PlayListUpdateSerializer)

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsModerator, )

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner | IsModerator, )

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsOwner, )

    def get_object(self):
        user = self.request.user
        return User.objects.get(id = user.id)

class UserPasswordUpdateAPIView(GenericAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = (IsOwner, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        old = serializer.validated_data['old_password']
        new = serializer.validated_data['new_password']
        
        if old == new:
            return Response({'error': 'Новый пароль должен отличаться от старого'}, status=400)

        user = request.user
        if not user.check_password(old):
            return Response({'error': 'Неверный старый пороль'}, status=400)
        
        user.set_password(new)
        user.save()
        return Response({'success': True})

class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsOwner | IsAdmin, )

class FollowToggleAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        follow, created = Follow.objects.get_or_create(
            follower = request.user,
            following=artist
        )
        if not created:
            follow.delete()
            return Response({"status": 'unfollowed'})
        return Response({"status": 'followed'})
    
class PlayListDetailAPIView(RetrieveAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        obj = super().get_object()
        if obj.is_public or obj.user == self.request.user:
            return obj
        raise PermissionDenied

class PlayListCreateAPIView(CreateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user= self.request.user)

class PlayListsUpdateAPIView(UpdateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return PlayList.objects.get(id = self.kwargs['pk'],user=self.request.user)
    
class PlayListDeleteAPIView(DestroyAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated | IsAdmin, )

    def get_object(self):
        return PlayList.objects.get(id = self.kwargs['pk'], user=self.request.user)
    
class PlayListAddTrackAPIView(GenericAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        playlist = get_object_or_404(PlayList, pk=pk, user=request.user)
        track = get_object_or_404(Track, pk=request.data.get('track_id'))
        obj, created = PlayListTrack.objects.get_or_create(playlist=playlist, track=track)
        if not created:
            return Response({'error': 'Трек уже в плейлисте'})
        return Response({'status': "added"})
    
class PlayListRemoveTrackAPIView(GenericAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated, )
    def post(self, request, pk):
        playlist = get_object_or_404(PlayList, pk=pk, user = request.user)
        PlayListTrack.objects.filter(
            playlist=playlist, 
            track_id=request.data.get('track_id')
        ).delete()
        return Response({'status': 'removed'})
