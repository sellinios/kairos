# api/serializers/serializer_geographic_level.py

from rest_framework import serializers
from geography.models import GeographicLevel

class GeographicLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicLevel
        fields = '__all__'
