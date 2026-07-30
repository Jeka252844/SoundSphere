from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView

from config import views

urlpatterns = [
    # pages
    path('', views.home, name='home'),
    path('docs/', views.docs, name='documentation'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('tracks/create/', views.track_create, name='track_create'),
    path('track/card/<int:track_id>/', views.track_card, name='track_card'),
    path('profile/', views.profile, name='profile'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/my/', views.my_playlists, name='my_playlist'),
    path('playlist/create/', views.playlist_create, name='playlist_create'),
    path('playlist/<int:playlist_id>/detail/', views.playlist_detail, name='playlist_detail'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('player/', views.player, name='player'),
    path('artists/', views.artists, name='artists'),
    path('artist/create/', views.artist_create, name='artist_create'),
    path('artist/my/', views.artist_profile_my_view, name='artist_profile_my'),
    path('artist/<int:artist_id>/', views.artist_profile_view, name='artist_profile'),
    path('album/create/', views.album_create, name='album_create'),
    path('album/<int:album_id>/', views.album, name='album'),

    # base_url
    path('admin/', admin.site.urls),

    # app urls
    path('users/', include('apps.users.urls', namespace='users')),
    path('api/tracks/', include('apps.tracks.urls')),
    path('api/artists/', include('apps.artists.urls')),
    path('api/social/', include('apps.social.urls')),

    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + (
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
