# api/serializers/serializer_geographic_continent.py

from rest_framework import serializers
from geography.models import GeographicContinent, GeographicCountry

class GeographicCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicCountry
        fields = ['id', 'name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'capital', 'official_languages', 'currency', 'area']

class GeographicContinentSerializer(serializers.ModelSerializer):
    countries = GeographicCountrySerializer(many=True, read_only=True)

    class Meta:
        model = GeographicContinent
        fields = ['id', 'name', 'slug', 'countries']
