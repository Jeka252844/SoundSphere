from rest_framework import serializers

from apps.users.models import PlayList

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('title', 'user', 'is_public', 'created_at')

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
