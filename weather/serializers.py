from rest_framework import serializers
from .models import GFSForecast, Place

class GFSForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFSForecast
        fields = ['id', 'temperature', 'precipitation', 'wind_speed', 'timestamp', 'place']

    def create(self, validated_data):
        """
        Custom create method, if needed, to handle specific logic
        """
        return GFSForecast.objects.create(**validated_data)