from rest_framework import serializers

from apps.artists.models import Artist
from apps.users.models import User

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', 'bio', 'avatar', 'user')

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