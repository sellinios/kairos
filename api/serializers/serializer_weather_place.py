from rest_framework import serializers
from geography.models import Place
from weather.models import GFSForecast

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'slug', 'longitude', 'latitude', 'elevation', 'category', 'admin_division']

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFSForecast
        fields = ['id', 'latitude', 'longitude', 'forecast_data', 'timestamp']