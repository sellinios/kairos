# In api/serializers/serializer_weather_places.py

from rest_framework import serializers
from weather.models.model_gfs_forecast import GFSForecast

class GFSForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFSForecast
        fields = '__all__'
