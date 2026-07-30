from rest_framework import serializers

from apps.users.models import PlayList
from apps.tracks.models import Track
from apps.tracks.track_serializer import TrackSerializer

class PlayListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes = serializers.SerializerMethodField()
    tracks_count =serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()

    class Meta:
        model = PlayList
        fields = ('id', 'title', 'user', 'is_public', 'created_at', 'likes', 'tracks_count', 'tracks')

    def get_likes(self, obj):
        return obj.playlist_like.count()

    def get_tracks_count(self, obj):
        return obj.playlist_track.count()

    def get_tracks(self, obj):
        track_ids = obj.playlist_track.values_list('track_id', flat=True)
        tracks = Track.objects.filter(id__in=track_ids)
        return TrackSerializer(tracks, many=True).data

class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('id', 'title', 'is_public', 'user') 
        extra_kwargs = {
            'title': {'required': True},
            'is_public': {'required': False},
            'user': {'read_only': True}, 
        }

    
class PlayListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('title','is_public')
        extra_kwargs = {
            'title': {'required': False},
            'is_public': {"required": False}
        }
