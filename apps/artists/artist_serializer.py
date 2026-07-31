from rest_framework import serializers

from apps.artists.models import Artist
from apps.artists.album_serializer import AlbumSerializer
from apps.tracks.track_serializer import TrackSerializer

class ArtistSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    albums = AlbumSerializer(many=True, read_only=True)
    tracks = TrackSerializer(many=True, read_only=True, source='track_set')
    class Meta:
        model = Artist
        fields = ('id', 'name', 'bio', 'avatar', 'user', 'albums', 'tracks', 'followers_count')

    def get_followers_count(self, obj):
        return obj.followers.count()

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