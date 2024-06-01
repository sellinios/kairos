from rest_framework import serializers
from geography.models import Continent

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = '__all__'  # Adjust fields as necessary
