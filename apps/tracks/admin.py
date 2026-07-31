from django.contrib import admin
from .models import Genre, Track, TrackLike

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'slug')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genre', 'plays_count', 'created_at')
    list_filter = ('genre',)

@admin.register(TrackLike)
class TrackLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at')
