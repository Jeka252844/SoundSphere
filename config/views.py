from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def docs(request):
    return render(request, 'document.html')

def tracks(request):
    return render(request, 'tracks.html')

def profile(request):
    return render(request, 'profile.html')

def playlist(request):
    return render(request, 'playlist.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def player(request):
    return render(request, 'player.html')

def artists(request):
    return render(request, 'artists.html')

def album(request):
    return render(request, 'album.html')