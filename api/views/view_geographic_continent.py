from rest_framework import viewsets
from geography.models import Continent
from api.serializers.serializer_geographic_continent import ContinentSerializer

class ContinentViewSet(viewsets.ModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer
