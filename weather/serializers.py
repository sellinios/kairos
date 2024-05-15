# weather/serializers.py
from rest_framework import serializers
from .models import GFSForecast

class GFSForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFSForecast
        fields = '__all__'
