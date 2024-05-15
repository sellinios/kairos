# geography/serializers.py
from rest_framework import serializers
from .models import Country, Region, RegionalUnit, Municipality, Place


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class RegionalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionalUnit
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'latitude', 'longitude', 'custom_id']