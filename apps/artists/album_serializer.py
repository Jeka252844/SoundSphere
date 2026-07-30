from rest_framework import serializers

from apps.artists.models import Album
from apps.tracks.track_serializer import TrackSerializer

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = ('id','title', 'artist', 'cover', 'release_date', 'tracks')
    
class AlbumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id','title', 'cover', 'release_date')
        extra_kwargs = {
            "title": {"required": True},
            "cover": {"required": False}
        }

    def create(self, validated_data):
        return super().create(validated_data)

class AlbumUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('title', 'cover')
        extra_kwargs = {
            "title": {"required": False},
            "cover": {"required": False}
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)