from rest_framework import serializers
from mutagen import File as MutagenFile

from apps.tracks.models import Track, Genre
from apps.artists.models import Album, Artist

class TrackSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    artist_id = serializers.IntegerField(source='artist.id', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    weekly_plays = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Track
        fields = (
            'id', 'title', 'duration', 'plays_count', 'cover', 
            'audio_file', 'created_at',
            # Вложенные
            'artist_id', 'artist_name',
            'album', 'genre_name',
            # Статистика
            'weekly_plays',
        )


class TrackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('title', 'album', 'genre', 'cover', 'audio_file')
        extra_kwargs = {
            'title': {'required': True},
            'album': {'required': True},
            'genre': {'required': True},
            'audio_file': {'required': True},
            'cover': {'required': False},
        }

    def create(self, validated_data):
        audio = validated_data['audio_file']
        if audio:
            try:
                audio_info = MutagenFile(audio)
                validated_data['duration'] = int(audio_info.info.length)
            except:
                validated_data['duration'] = 0
        return super().create(validated_data)
    
class TrackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('title', 'album', 'cover', 'audio_file', 'genre')
        read_only_fields = ('duration', 'plays_count')
        extra_kwargs = {
            'title': {'required': False},
            'album': {'required': False},
            'cover': {'required': False},
            'audio_file': {'required': False},
            'genre': {'required': False},
        }

    def update(self, instance, validated_data):
        audio = validated_data.get('audio_file')
        if audio:
            try:
                audio_info = MutagenFile(audio)
                validated_data['duration']= int(audio_info.info.length)
            except:
                validated_data['duration'] = 0
        return super().update(instance, validated_data)