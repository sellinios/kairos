# weather/views.py
from rest_framework import generics
from .models import GFSForecast
from .serializers import GFSForecastSerializer

class GFSForecastListView(generics.ListCreateAPIView):
    queryset = GFSForecast.objects.all()
    serializer_class = GFSForecastSerializer
