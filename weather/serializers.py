from rest_framework import serializers
from .models import GFSForecast, MetarData

from rest_framework import serializers
from .models import GFSForecast

class GFSForecastSerializer(serializers.ModelSerializer):
    temperature = serializers.FloatField(source='rounded_temperature')

    class Meta:
        model = GFSForecast
        fields = ['id', 'temperature', 'precipitation', 'wind_speed', 'timestamp', 'place']

class MetarDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetarData
        fields = '__all__'
