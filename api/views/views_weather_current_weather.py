from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Func
from django.utils import timezone
from weather.models import GFSForecast
from ..serializers import GFSForecastSerializer

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s as numeric), 1)'

class CurrentWeatherView(APIView):
    @staticmethod
    def get(request, *_):
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
