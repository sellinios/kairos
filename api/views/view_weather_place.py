from rest_framework import viewsets
from weather.models import GFSForecast
from api.serializers.serializer_weather_place import WeatherSerializer

class WeatherPlaceViewSet(viewsets.ModelViewSet):
    queryset = GFSForecast.objects.all()
    serializer_class = WeatherSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
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

        point = Point(longitude, latitude, srid=4326)

        # Find the nearest forecast
        nearest_forecast = GFSForecast.objects.annotate(distance=Distance('location', point)).order_by('distance').first()

        if not nearest_forecast:
            logger.debug(f"No weather data found for nearest location: ({latitude}, {longitude})")
            return Response({"error": "Weather data not found for the nearest location."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WeatherSerializer(nearest_forecast)
        return Response(serializer.data, status=status.HTTP_200_OK)
