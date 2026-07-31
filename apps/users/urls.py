from django.urls import path
from apps.users.views import (UserListAPIView, UserCreateAPIView, UserDetailAPIView, 
UserPasswordUpdateAPIView, UserDeleteAPIView, UserUpdateAPIView, FollowToggleAPIView,
PlayListDetailAPIView, PlayListCreateAPIView, PlayListsUpdateAPIView, PlayListDeleteAPIView,
PlayListAddTrackAPIView, PlayListRemoveTrackAPIView, PlayListListAPIView, PlayListLikeAPIView,
TopPlaylistsWeeklyView, PlaylistLikeCheckAPIView, verify_email)

app_name= 'users'

urlpatterns = [
    # user
    path('list/', UserListAPIView.as_view(), name='user_list'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('update/', UserUpdateAPIView.as_view(), name='update_user'),
    path('password/update/', UserPasswordUpdateAPIView.as_view(), name='update_password'),
    path('<int:pk>/delete/', UserDeleteAPIView.as_view(), name='delete_user'),

    # verify-email
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),

    # follow
    path('<int:pk>/follow/', FollowToggleAPIView.as_view(), name='follow'),

    # playlist
    path('playlist/list/', PlayListListAPIView.as_view(), name='playlist_list'),
    path('playlist/<int:pk>/', PlayListDetailAPIView.as_view(), name='playlist_detail'),
    path('playlist/create/', PlayListCreateAPIView.as_view(), name='playlist_create'),
    path('playlist/<int:pk>/update/', PlayListsUpdateAPIView.as_view(), name='playlist_update'),
    path('playlist/<int:pk>/delete/', PlayListDeleteAPIView.as_view(), name='playlist_delete'),
    path('playlist/<int:pk>/add/', PlayListAddTrackAPIView.as_view(), name='playlist_add'),
    path('playlist/<int:pk>/remove/', PlayListRemoveTrackAPIView.as_view(), name='playlist_remove'),
    path('playlist/<int:pk>/like/', PlayListLikeAPIView.as_view(), name='playlist_like'),
    path('playlist/<int:pk>/like/check/', PlaylistLikeCheckAPIView.as_view(), name='playlist_like_check'),
    path('playlist/top/', TopPlaylistsWeeklyView.as_view(), name='top_weekly_playlists')
]