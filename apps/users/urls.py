from django.urls import path
from apps.users.views import (UserListAPIView, UserCreateAPIView, UserDetailAPIView, 
UserPasswordUpdateAPIView, UserDeleteAPIView, UserUpdateAPIView, FollowToggleAPIView,
PlayListDetailAPIView, PlayListCreateAPIView, PlayListsUpdateAPIView, PlayListDeleteAPIView)

app_name= 'users'

urlpatterns = [
    # user
    path('', UserListAPIView.as_view(), name='user_list'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('update/', UserUpdateAPIView.as_view(), name='update_user'),
    path('password/update/', UserPasswordUpdateAPIView.as_view(), name='update_password'),
    path('<int:pk>/delete/', UserDeleteAPIView.as_view(), name='delete_user'),

    # follow
    path('<int:pk>/follow/', FollowToggleAPIView.as_view(), name='follow'),

    # playlist
    path('playlist/<int:pk>/', PlayListDetailAPIView.as_view(), name='playlist_detail'),
    path('playlist/create/', PlayListCreateAPIView.as_view(), name='palylist_create'),
    path('playlist/<int:pk>/update/', PlayListsUpdateAPIView.as_view(), name='playlist_update'),
    path('playlist/<int:pk>/delete/', PlayListDeleteAPIView.as_view(), name='playlist_delete'),
]