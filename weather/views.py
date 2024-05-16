from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GFSForecast
from .serializers import GFSForecastSerializer
from django.utils import timezone

class WeatherListView(APIView):
    def get(self, request, format=None):
        forecasts = GFSForecast.objects.all()
        serializer = GFSForecastSerializer(forecasts, many=True)
        return Response(serializer.data)

class CurrentWeatherView(APIView):
    def get(self, request, format=None):
        location = request.query_params.get('location', 'Vyronas')
        current_time = timezone.now()
        recent_forecast = GFSForecast.objects.filter(place__name=location, timestamp__lte=current_time).order_by('-timestamp').first()
        serializer = GFSForecastSerializer(recent_forecast)
        return Response(serializer.data)
