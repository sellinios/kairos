from rest_framework import serializers
from geography.models import Place
from weather.models import GFSForecast  # Adjust the import based on your actual model

class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Place model.
    """
    class Meta:
        model = Place
        fields = ['id', 'name', 'slug', 'longitude', 'latitude', 'elevation', 'category', 'admin_division']

class WeatherSerializer(serializers.ModelSerializer):
    """
    Serializer class for the GFSForecast model.
    """
    place = PlaceSerializer()

    class Meta:
        model = GFSForecast  # Adjust based on your actual model
        fields = '__all__'
