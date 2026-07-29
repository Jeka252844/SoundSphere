from rest_framework import serializers

from apps.artists.models import Artist
from apps.artists.album_serializer import AlbumSerializer
from apps.tracks.track_serializer import TrackSerializer

class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)
    tracks = TrackSerializer(many=True, read_only=True, source='track_set')
    class Meta:
        model = Artist
        fields = ('id', 'name', 'bio', 'avatar', 'user', 'albums', 'tracks')

class ArtistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', 'bio', 'avatar')
        extra_kwargs = {
            "name": {'required': True},
            "bio": {'required': False},
            "avatar": {'required': False}
        }

    def create(self, validated_data):
        return super().create(validated_data)
    
class ArtistUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', 'bio', 'avatar')
        extra_kwargs = {
            "name": {'required': False},
            "bio": {'required': False},
            "avatar": {'required': False}
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)