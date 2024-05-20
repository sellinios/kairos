from rest_framework import viewsets
from geography.models import AdministrativeDivision
from ..serializers import AdministrativeDivisionSerializer

class AdministrativeDivisionViewSet(viewsets.ModelViewSet):
    queryset = AdministrativeDivision.objects.all()
    serializer_class = AdministrativeDivisionSerializer
