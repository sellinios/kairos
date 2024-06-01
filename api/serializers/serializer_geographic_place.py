# api/serializers/serializer_geographic_place.py
from rest_framework import serializers
from geography.models import GeographicPlace

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicPlace
        fields = '__all__'  # Adjust fields as necessary