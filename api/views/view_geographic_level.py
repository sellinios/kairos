# api/views/view_geographic_level.py

from rest_framework import generics
from geography.models import GeographicLevel
from api.serializers.serializer_geographic_level import GeographicLevelSerializer

class GeographicLevelListView(generics.ListCreateAPIView):
    queryset = GeographicLevel.objects.all()
    serializer_class = GeographicLevelSerializer

class GeographicLevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeographicLevel.objects.all()
    serializer_class = GeographicLevelSerializer
    lookup_field = 'id'
