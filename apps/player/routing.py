from django.urls import path
from .consumers import PlayerConsumer

websocket_urlpatterns = [
    path('ws/player/', PlayerConsumer.as_asgi()),
]