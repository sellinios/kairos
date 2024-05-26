from rest_framework import serializers
from geography.models.model_geographic_country import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'slug', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'capital', 'official_languages', 'currency', 'area', 'continent']
