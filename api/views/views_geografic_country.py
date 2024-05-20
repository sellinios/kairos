from rest_framework import viewsets
from geography.models import Country
from ..serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
