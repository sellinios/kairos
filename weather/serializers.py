from rest_framework import serializers
from .models import GFSForecast, MetarData

class GFSForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFSForecast
        fields = '__all__'

class MetarDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetarData
        fields = '__all__'
