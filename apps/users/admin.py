from django.contrib import admin
from .models import User, PlayList, PlayListTrack, PlayListLike, Follow, EmailVerificationToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_role', 'is_artist', 'is_active')
    list_filter = ('user_role', 'is_artist', 'is_active')
    search_fields = ('username', 'email')

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'created_at')

@admin.register(PlayListTrack)
class PlayListTrackAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'track')

@admin.register(PlayListLike)
class PlayListLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'playlist', 'liked_at')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
