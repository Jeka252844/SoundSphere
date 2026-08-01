from rest_framework.generics import (
    ListAPIView, CreateAPIView, GenericAPIView,
    UpdateAPIView, DestroyAPIView, RetrieveAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
import threading

from apps.users.models import User, Follow, PlayList, PlayListTrack, PlayListLike, EmailVerificationToken
from apps.artists.models import Artist
from apps.tracks.models import Track
from apps.users.permissions import IsAdmin, IsModerator, IsOwner

from apps.users.user_serializer import (
    UserSerializer, UserCreateSerializer,
    UserUpdateSerializer, UserPasswordSerializer
)
from apps.users.playlist_serializer import (
    PlayListSerializer, PlayListCreateSerializer, PlayListUpdateSerializer
)
from apps.users.services import PlaylistService, UserService


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsModerator, )


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = EmailVerificationToken.objects.create(user=user)

        verify_url = f'{settings.SITE_URL}/users/verify-email/{token.token}/'

        email = EmailMessage(
            'Подтверждение почты SoundSphere',
            f'Перейдите по ссылке:\n\n{verify_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        email.send(fail_silently=False)
        threading.Thread(target=UserService.delete_unverified_user, args=(user.id, ), daemon=True).start()


def verify_email(request, token):
    try:
        verification = EmailVerificationToken.objects.get(token=token)
        verification.user.is_active = True
        verification.user.save()
        verification.delete()

        return HttpResponse('''
            <script>
                localStorage.setItem('email_verified', 'true');
                window.close();
            </script>
            <h2>Успешная регистрация</h2>
        ''')
    except EmailVerificationToken.DoesNotExist:
        return HttpResponse('''
            <div style="text-align:center;padding:50px;background:#111;color:#fff;min-height:100vh;">
                <h2 style="color:#ef4444;">❌ Неверная или устаревшая ссылка</h2>
            </div>
        ''')


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
        return User.objects.get(id=user.id)

    def update(self, request, *args, **kwargs):
        partial = True
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserPasswordUpdateAPIView(GenericAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = (IsOwner, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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
            follower=request.user,
            following=artist
        )
        if not created:
            follow.delete()
            return Response({"status": 'unfollowed'})
        return Response({"status": 'followed'})


class PlayListListAPIView(ListAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = (IsModerator, )


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
        serializer.save(user=self.request.user)


class PlayListsUpdateAPIView(UpdateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return PlayList.objects.get(id=self.kwargs['pk'], user=self.request.user)


class PlayListDeleteAPIView(DestroyAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated | IsAdmin, )

    def get_object(self):
        return PlayList.objects.get(id=self.kwargs['pk'], user=self.request.user)


class PlayListAddTrackAPIView(GenericAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        playlist = get_object_or_404(PlayList, pk=pk, user=request.user)
        track = get_object_or_404(Track, pk=request.data.get('track_id'))
        obj, created = PlayListTrack.objects.get_or_create(playlist=playlist, track=track)
        if not created:
            return Response({'error': 'Трек уже в плейлисте'}, status=status.HTTP_409_CONFLICT)
        return Response({'status': "added"})


class PlayListRemoveTrackAPIView(GenericAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        playlist = get_object_or_404(PlayList, pk=pk, user=request.user)
        PlayListTrack.objects.filter(
            playlist=playlist,
            track_id=request.data.get('track_id')
        ).delete()
        return Response({'status': 'removed'})


class PlayListLikeAPIView(GenericAPIView):
    queryset = PlayList.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        playlist = get_object_or_404(PlayList, pk=pk)
        like, created = PlayListLike.objects.get_or_create(
            playlist=playlist, user=request.user
        )

        if not created:
            like.delete()
            return Response({'status': 'unliked', 'likes': playlist.playlist_like.count()})

        return Response({'status': 'liked', 'likes': playlist.playlist_like.count()})


class PlaylistLikeCheckAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'is_liked': False})

        playlist = get_object_or_404(PlayList, pk=pk)
        is_liked = PlayListLike.objects.filter(playlist=playlist, user_id=user_id).exists()
        return Response({'is_liked': is_liked})


class TopPlaylistsWeeklyView(ListAPIView):
    serializer_class = PlayListSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return PlaylistService.top_weekly_playlists()
