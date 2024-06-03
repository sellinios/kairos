# api/views/view_geographic_continent.py

from rest_framework import generics
from geography.models import GeographicContinent
from api.serializers.serializer_geographic_continent import GeographicContinentSerializer

class GeographicContinentListView(generics.ListAPIView):
    queryset = GeographicContinent.objects.all()
    serializer_class = GeographicContinentSerializer

class GeographicContinentDetailView(generics.RetrieveAPIView):
    queryset = GeographicContinent.objects.all()
    serializer_class = GeographicContinentSerializer
    lookup_field = 'slug'
