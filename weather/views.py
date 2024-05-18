from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GFSForecast
from .serializers import GFSForecastSerializer
from django.db.models import F, Func, Value
from django.db.models.functions import Cast

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s as numeric), 1)'

class WeatherListView(APIView):
    def get(self, request, format=None):
        # Annotate the queryset with rounded temperature values
        forecasts = GFSForecast.objects.annotate(rounded_temperature=Round(F('temperature')))
        serializer = GFSForecastSerializer(forecasts, many=True)
        return Response(serializer.data)

class CurrentWeatherView(APIView):
    def get(self, request, format=None):
        current_time = timezone.now()
        # Fetch the most recent forecast without filtering by location
        recent_forecast = GFSForecast.objects.filter(timestamp__lte=current_time).annotate(rounded_temperature=Round(F('temperature'))).order_by('-timestamp').first()
        serializer = GFSForecastSerializer(recent_forecast)
        return Response(serializer.data)
