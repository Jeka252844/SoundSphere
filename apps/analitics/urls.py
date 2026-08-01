from django.urls import path
from .views import CurrentListeningView

urlpatterns = [
    path('current/', CurrentListeningView.as_view(), name='current-listening'),
]
