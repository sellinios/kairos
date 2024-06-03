# api/views/view_geographic_country.py
from rest_framework import generics
from geography.models import GeographicCountry
from api.serializers.serializer_geographic_country import GeographicCountrySerializer

class GeographicCountryListView(generics.ListAPIView):
    queryset = GeographicCountry.objects.all()
    serializer_class = GeographicCountrySerializer

class GeographicCountryDetailView(generics.RetrieveAPIView):
    queryset = GeographicCountry.objects.all()
    serializer_class = GeographicCountrySerializer
    lookup_field = 'slug'
