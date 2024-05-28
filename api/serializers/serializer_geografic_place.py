"""
This module defines serializers for the Place, Category, and AdminDivisionInstance models.
"""

from rest_framework import serializers
from geography.models import Place, Category, AdminDivisionInstance

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

class AdminDivisionInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer class for the AdminDivisionInstance model.
    """
    parent = serializers.PrimaryKeyRelatedField(queryset=AdminDivisionInstance.objects.all(), allow_null=True, required=False)

    class Meta:
        model = AdminDivisionInstance
        fields = ['id', 'name', 'level', 'slug', 'parent']

class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Place model.
    """
    category = CategorySerializer()
    admin_division = AdminDivisionInstanceSerializer()
    url = serializers.SerializerMethodField()
    weather_url = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = [
            'id', 'longitude', 'latitude', 'elevation',
            'category', 'admin_division', 'url', 'weather_url'
        ]

    def get_url(self, obj):
        return obj.get_full_url()

    def get_weather_url(self, obj):
        return obj.get_weather_url()

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        admin_division_data = validated_data.pop('admin_division')
        category, _ = Category.objects.get_or_create(**category_data)
        admin_division, _ = AdminDivisionInstance.objects.get_or_create(**admin_division_data)
        place = Place.objects.create(
            category=category,
            admin_division=admin_division,
            **validated_data
        )
        return place

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        admin_division_data = validated_data.pop('admin_division')
        category, _ = Category.objects.get_or_create(**category_data)
        admin_division, _ = AdminDivisionInstance.objects.get_or_create(**admin_division_data)

        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.elevation = validated_data.get('elevation', instance.elevation)
        instance.category = category
        instance.admin_division = admin_division
        instance.save()
        return instance
