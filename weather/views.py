from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GFSForecast, MetarData
from .serializers import GFSForecastSerializer, MetarDataSerializer
from django.db.models import F, Func
from django.utils import timezone

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s as numeric), 1)'

class WeatherListView(APIView):
    def get(self, request, format=None):
        forecasts = GFSForecast.objects.annotate(rounded_temperature=Round(F('temperature')))
        serializer = GFSForecastSerializer(forecasts, many=True)
        return Response(serializer.data)

class CurrentWeatherView(APIView):
    def get(self, request, format=None):
        current_time = timezone.now()
        recent_forecast = GFSForecast.objects.filter(timestamp__lte=current_time).annotate(rounded_temperature=Round(F('temperature'))).order_by('-timestamp').first()
        serializer = GFSForecastSerializer(recent_forecast)
        return Response(serializer.data)

class MetarListView(APIView):
    def get(self, request, format=None):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        metar_data = MetarData.objects.filter(station__latitude=latitude, station__longitude=longitude).order_by('-metar_timestamp')
        serializer = MetarDataSerializer(metar_data, many=True)
        return Response(serializer.data)
