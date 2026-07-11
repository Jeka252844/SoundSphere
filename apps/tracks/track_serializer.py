from rest_framework import serializers
from mutagen.mp3 import MP3

from apps.tracks.models import Track, Genre
from apps.artists.models import Album, Artist

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('id', 'title', 'artist', 'album', 'cover', 'audio_file', 'genre', 'duration', 'plays_count', 'created_at')


class TrackCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    audio_file = serializers.FileField(required=True)
    album = serializers.PrimaryKeyRelatedField(queryset= Album.objects.all(), required= False, allow_null= True)
    artist = serializers.PrimaryKeyRelatedField(queryset= Artist.objects.all(), required= True)
    genre = serializers.PrimaryKeyRelatedField(queryset= Genre.objects.all(), required= False, allow_null= True)
    cover = serializers.ImageField(required= False)
    class Meta:
        model = Track
        fields = ('title', 'artist', 'album', 'genre', 'cover', 'audio_file')

    def create(self, validated_data):
        audio = validated_data['audio_file']
        audio_info = MP3(audio)
        validated_data['duration'] = int(audio_info.info.length)
        return super().create(validated_data)
    
class TrackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('title', 'artist', 'album', 'cover', 'audio_file', 'genre')
        read_only_fields = ('duration', 'plays_count')

    def update(self, instance, validated_data):
        if validated_data['audio_file']:
            audio = validated_data['audio_file']
            audio_info = MP3(audio)
            validated_data['duration']= int(audio_info.info.length)
        return super().update(instance, validated_data)