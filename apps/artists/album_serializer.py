from rest_framework import serializers

from apps.artists.models import Album
from apps.tracks.track_serializer import TrackSerializer

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Album
        fields = ('id','title', 'artist', 'artist_name', 'cover', 'release_date', 'tracks', 'likes')

    def get_likes(self, obj):
        return obj.album_like.count()

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