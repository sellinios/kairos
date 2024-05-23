from rest_framework import serializers
from geography.models import Place, Category, AdminDivisionInstance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdminDivisionInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDivisionInstance
        fields = ['id', 'name', 'level']


class PlaceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    admin_division = AdminDivisionInstanceSerializer()

    class Meta:
        model = Place
        fields = ['id', 'longitude', 'latitude', 'height', 'category', 'admin_division']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        admin_division_data = validated_data.pop('admin_division')
        category, created = Category.objects.get_or_create(**category_data)
        admin_division, created = AdminDivisionInstance.objects.get_or_create(**admin_division_data)
        place = Place.objects.create(category=category, admin_division=admin_division, **validated_data)
        return place

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        admin_division_data = validated_data.pop('admin_division')
        category, created = Category.objects.get_or_create(**category_data)
        admin_division, created = AdminDivisionInstance.objects.get_or_create(**admin_division_data)

        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.height = validated_data.get('height', instance.height)
        instance.category = category
        instance.admin_division = admin_division
        instance.save()
        return instance
