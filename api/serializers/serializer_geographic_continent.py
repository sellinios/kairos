"""
This module defines serializers for the Continent and Country models.
"""

from rest_framework import serializers
from geography.models import Continent, Country

class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Country model.
    """
    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = Country
        fields = [
            'id', 'name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric',
            'capital', 'official_languages', 'currency', 'area', 'slug'
        ]

class ContinentSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Continent model.
    """
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = Continent
        fields = ['id', 'name', 'slug', 'countries']
