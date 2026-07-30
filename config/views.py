from django.shortcuts import render
from apps.tracks.models import Track

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def docs(request):
    return render(request, 'document.html')

def tracks(request):
    return render(request, 'tracks.html')

def track_create(request):
    return render(request, 'track_create.html')

def track_card(request, track_id):
    return render(request, 'track_card.html', {'track_id': track_id})

def profile(request):
    return render(request, 'profile.html')

def playlist(request):
    return render(request, 'playlist.html')

def playlist_detail(request, playlist_id):
    return render(request, 'playlist_detail.html', {'playlist_id': playlist_id})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def player(request):
    track_id = request.GET.get('track_id', 1)
    track = Track.objects.filter(id=track_id).first()
    return render(request, 'player.html', {'track': track})

def artists(request):
    return render(request, 'artists.html')

def artist_create(request):
    return render(request, 'artist_create.html')

def artist_profile_my_view(request):
    return render(request, 'artist_profile.html', {'is_my': True})

def artist_profile_view(request, artist_id):
    return render(request, 'artist_profile.html', {'artist_id': artist_id, 'is_my': False})

def album(request, album_id):
    return render(request, 'album.html', {'album_id': album_id})

def album_create(request):
    return render(request, 'album_create.html')