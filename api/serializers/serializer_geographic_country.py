# api/serializers/serializer_geographic_country.py
from rest_framework import serializers
from geography.models import GeographicCountry

class GeographicCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicCountry
        fields = '__all__'
