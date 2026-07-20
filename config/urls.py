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
    path('profile/', views.profile, name='profile'),
    path('playlist/', views.playlist, name='playlist'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('player/', views.player, name='player'),
    path('artists/', views.artists, name='artists'),
    path('album/', views.album, name='album'),

    # base_url
    path('admin/', admin.site.urls),

    # app urls
    path('users/', include('apps.users.urls', namespace='users')),
    path('api/tracks/', include('apps.tracks.urls')),
    path('api/artists/', include('apps.artists.urls')),

    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
