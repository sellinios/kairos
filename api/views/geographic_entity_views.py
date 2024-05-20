from rest_framework import viewsets
from geography.models import GeographicEntity
from ..serializers import GeographicEntitySerializer

class GeographicEntityViewSet(viewsets.ModelViewSet):
    queryset = GeographicEntity.objects.all()
    serializer_class = GeographicEntitySerializer
