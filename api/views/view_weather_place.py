from rest_framework import viewsets
from weather.models import GFSForecast
from api.serializers.serializer_weather_place import WeatherSerializer

class WeatherPlaceViewSet(viewsets.ModelViewSet):
    queryset = GFSForecast.objects.all()
    serializer_class = WeatherSerializer

# Ensure DynamicWeatherView is also defined correctly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.nearest_place import find_nearest_place
import logging

logger = logging.getLogger(__name__)

class DynamicWeatherView(APIView):
    def get(self, request, continent, country, region, subregion, city):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response({"error": "Latitude and longitude are required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response({"error": "Invalid latitude or longitude."}, status=status.HTTP_400_BAD_REQUEST)

        nearest_place = find_nearest_place(latitude, longitude)
        if not nearest_place:
            return Response({"error": "No nearby place found."}, status=status.HTTP_404_NOT_FOUND)

        logger.debug(f"Nearest place found: {nearest_place.name} ({nearest_place.latitude}, {nearest_place.longitude})")

        # Find forecasts near the nearest place
        weather_data = GFSForecast.objects.filter(
            latitude=nearest_place.latitude, longitude=nearest_place.longitude
        )
        if not weather_data.exists():
            logger.debug(f"No weather data found for nearest place: {nearest_place.name} ({nearest_place.latitude}, {nearest_place.longitude})")
            return Response({"error": "Weather data not found for the nearest place."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WeatherSerializer(weather_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
