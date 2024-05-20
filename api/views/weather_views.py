from rest_framework import viewsets
from weather.models import GFSForecast, MetarData
from ..serializers import GFSForecastSerializer, MetarDataSerializer

class GFSForecastViewSet(viewsets.ModelViewSet):
    queryset = GFSForecast.objects.all()
    serializer_class = GFSForecastSerializer

class MetarDataViewSet(viewsets.ModelViewSet):
    queryset = MetarData.objects.all()
    serializer_class = MetarDataSerializer
