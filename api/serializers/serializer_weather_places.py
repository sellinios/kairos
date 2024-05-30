# api/serializers/serializer_weather_places.py

from rest_framework import serializers
from weather.models.model_gfs_forecast import GFSForecast
import math

class GFSForecastSerializer(serializers.ModelSerializer):
    temperature_celsius = serializers.SerializerMethodField()
    wind_speed = serializers.SerializerMethodField()
    wind_direction = serializers.SerializerMethodField()

    class Meta:
        model = GFSForecast
        fields = '__all__'

    def get_temperature_celsius(self, obj):
        return obj.forecast_data["temperature_level_0_surface"] - 273.15

    def get_wind_speed(self, obj):
        u = obj.forecast_data["u-component_of_wind_level_10_heightAboveGround"]
        v = obj.forecast_data["v-component_of_wind_level_10_heightAboveGround"]
        return math.sqrt(u**2 + v**2)

    def get_wind_direction(self, obj):
        u = obj.forecast_data["u-component_of_wind_level_10_heightAboveGround"]
        v = obj.forecast_data["v-component_of_wind_level_10_heightAboveGround"]
        direction = (math.atan2(v, u) * 180 / math.pi + 360) % 360
        return direction
