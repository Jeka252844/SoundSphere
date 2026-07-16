from rest_framework import serializers

from apps.users.models import PlayList

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('name', 'user', 'is_public', 'created_at')

class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('name','is_public')
        extra_kwargs = {
            'name': {'required': True},
            'is_public': {"required": False}
        }
    
    def create(self, validated_data):
        return super().create(validated_data)
    
class PlayListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('name','is_public')
        extra_kwargs = {
            'name': {'required': False},
            'is_public': {"required": False}
        }
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)