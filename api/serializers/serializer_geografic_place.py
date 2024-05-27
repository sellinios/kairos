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
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = Category
        fields = ['id', 'name']

class AdminDivisionInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer class for the AdminDivisionInstance model.
    """
    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = AdminDivisionInstance
        fields = ['id', 'name', 'level']

class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Place model.
    """
    category = CategorySerializer()
    admin_division = AdminDivisionInstanceSerializer()

    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = Place
        fields = [
            'id', 'longitude', 'latitude', 'height',
            'category', 'admin_division'
        ]

    def create(self, validated_data):
        """
        Create and return a new Place instance, given the validated data.
        """
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
        """
        Update and return an existing Place instance, given the validated data.
        """
        category_data = validated_data.pop('category')
        admin_division_data = validated_data.pop('admin_division')
        category, _ = Category.objects.get_or_create(**category_data)
        admin_division, _ = AdminDivisionInstance.objects.get_or_create(**admin_division_data)

        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.height = validated_data.get('height', instance.height)
        instance.category = category
        instance.admin_division = admin_division
        instance.save()
        return instance
