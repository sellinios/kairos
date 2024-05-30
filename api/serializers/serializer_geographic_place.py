# api/serializers/serializer_geographic_place.py
from rest_framework import serializers
from geography.models import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'  # Adjust fields as necessary
