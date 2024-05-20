from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Func
from weather.models import GFSForecast
from ..serializers import GFSForecastSerializer

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s as numeric), 1)'

class WeatherListView(APIView):
    @staticmethod
    def get(request):
        try:
            forecasts = GFSForecast.objects.annotate(rounded_temperature=Round(F('temperature')))
            serializer = GFSForecastSerializer(forecasts, many=True)
            return Response(serializer.data)
        except GFSForecast.DoesNotExist:
            return Response({'error': 'No forecast data found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
