from rest_framework import viewsets
from weather.models import MetarData
from ..serializers import MetarDataSerializer


class MetarDataViewSet(viewsets.ModelViewSet):
    queryset = MetarData.objects.all()
    serializer_class = MetarDataSerializer
