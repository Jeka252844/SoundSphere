from django.contrib import admin
from .models import Artist, Album, AlbumLike


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'followers_display')
    search_fields = ('name',)

    @admin.display(description='Подписчиков')
    def followers_display(self, obj):
        return obj.followers.count()


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')


@admin.register(AlbumLike)
class AlbumLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'liked_at')
