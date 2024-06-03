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
        temperature_kelvin = obj.forecast_data.get("temperature_level_2_heightAboveGround")
        if temperature_kelvin is not None:
            return temperature_kelvin - 273.15
        return None  # or some default value, e.g., 0 or a specific error message

    def get_wind_speed(self, obj):
        u = obj.forecast_data.get("u-component_of_wind_level_10_heightAboveGround")
        v = obj.forecast_data.get("v-component_of_wind_level_10_heightAboveGround")
        if u is not None and v is not None:
            return math.sqrt(u**2 + v**2)
        return None  # or some default value

    def get_wind_direction(self, obj):
        u = obj.forecast_data.get("u-component_of_wind_level_10_heightAboveGround")
        v = obj.forecast_data.get("v-component_of_wind_level_10_heightAboveGround")
        if u is not None and v is not None:
            direction = (math.atan2(v, u) * 180 / math.pi + 360) % 360
            return direction
        return None  # or some default value
