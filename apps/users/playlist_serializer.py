from rest_framework import serializers

from apps.users.models import PlayList

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        user = serializers.StringRelatedField()
        likes = serializers.SerializerMethodField()
        tracks_count =serializers.SerializerMethodField()

        model = PlayList
        fields = ('id', 'title', 'user', 'is_public', 'created_at', 'likes', 'tracks_count')

    def get_likes(self, obj):
        return obj.playlist_like.count()

    def get_tracks_count(self, obj):
        return obj.playlist_track.count()

class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('title','is_public')
        extra_kwargs = {
            'title': {'required': True},
            'is_public': {"required": False}
        }

    
class PlayListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('title','is_public')
        extra_kwargs = {
            'title': {'required': False},
            'is_public': {"required": False}
        }
