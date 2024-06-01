from rest_framework import viewsets
from geography.models import GeographicContinent
from api.serializers.serializer_geographic_continent import ContinentSerializer

class ContinentViewSet(viewsets.ModelViewSet):
    queryset = GeographicContinent.objects.all()
    serializer_class = ContinentSerializer
