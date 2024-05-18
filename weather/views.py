from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import GFSForecast, MetarData
from .serializers import GFSForecastSerializer, MetarDataSerializer
from django.db.models import F, Func
from django.utils import timezone

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s as numeric), 1)'

class WeatherListView(APIView):
    def get(self, request, format=None):
        try:
            forecasts = GFSForecast.objects.annotate(rounded_temperature=Round(F('temperature')))
            serializer = GFSForecastSerializer(forecasts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class CurrentWeatherView(APIView):
    def get(self, request, format=None):
        try:
            current_time = timezone.now()
            recent_forecast = GFSForecast.objects.filter(timestamp__lte=current_time).annotate(
                rounded_temperature=Round(F('temperature'))).order_by('-timestamp').first()
            if recent_forecast is None:
                return Response({'error': 'No recent forecast data found'}, status=404)
            serializer = GFSForecastSerializer(recent_forecast)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class MetarListView(APIView):
    def get(self, request, format=None):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return Response({'error': 'Latitude and longitude parameters are required.'}, status=400)

        try:
            metar_data = MetarData.objects.filter(station__latitude=latitude, station__longitude=longitude).order_by(
                '-metar_timestamp')
            if not metar_data.exists():
                return Response({'error': 'No METAR data found for the given coordinates'}, status=404)
            serializer = MetarDataSerializer(metar_data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
