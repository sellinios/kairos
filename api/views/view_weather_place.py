from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from weather.models import GFSForecast
from api.serializers.serializer_weather_place import WeatherSerializer

class DynamicWeatherView(APIView):
    def get(self, request, continent, country, region, subregion, city):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response({"error": "Latitude and longitude are required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            weather_data = GFSForecast.objects.get(latitude=latitude, longitude=longitude)
            serializer = WeatherSerializer(weather_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GFSForecast.DoesNotExist:
            return Response({"error": "Weather data not found"}, status=status.HTTP_404_NOT_FOUND)
