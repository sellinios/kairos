from rest_framework import viewsets
from geography.models.model_geographic_country import Country
from api.serializers.serializer_geographic_country import CountrySerializer

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'slug'
