# api/serializers/serializer_geographic_continent.py
from rest_framework import serializers
from geography.models import Continent, Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'capital', 'official_languages', 'currency', 'area']

class ContinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Continent
        fields = ['id', 'name', 'slug', 'countries']
