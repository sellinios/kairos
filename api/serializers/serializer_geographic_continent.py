# api/serializers/serializer_geographic_continent.py
from rest_framework import serializers
from geography.models import GeographicContinent


class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicContinent
        fields = '__all__'  # Adjust fields as necessary
