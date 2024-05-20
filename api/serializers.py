from rest_framework import serializers
from geography.models import Country, AdministrativeDivision, GeographicEntity, Place
from weather.models import GFSForecast, MetarData

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class AdministrativeDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeDivision
        fields = '__all__'

class GeographicEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicEntity
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = '__all__'

    def get_location(self, obj):
        return {
            'latitude': obj.location.y,
            'longitude': obj.location.x
        }

class GFSForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = GFSForecast
        fields = '__all__'

class MetarDataSerializer(serializers.ModelSerializer):
    temperature = serializers.FloatField()
    wind_speed = serializers.FloatField()
    conditions = serializers.CharField()

    class Meta:
        model = MetarData
        fields = ['station', 'metar_text', 'metar_timestamp', 'temperature', 'wind_speed', 'conditions']
