from django.urls import path
from apps.users.views import (UserListAPIView, UserCreateAPIView, UserRetrieveAPIView, 
UserPasswordUpdateAPIView, UserDeleteAPIView, UserUpdateAPIView, FollowToggleAPIView)

app_name= 'users'

urlpatterns = [
    # user
    path('', UserListAPIView.as_view(), name='user_list'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/', UserUpdateAPIView.as_view(), name='update_user'),
    path('password/update/', UserPasswordUpdateAPIView.as_view(), name='update_password'),
    path('<int:pk>/delete/', UserDeleteAPIView.as_view(), name='delete_user'),

    # follow
    path('<int:pk>/follow/', FollowToggleAPIView.as_view(), name='follow')
]