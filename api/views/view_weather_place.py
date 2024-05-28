from rest_framework import viewsets
from weather.models import GFSForecast  # Ensure correct imports
from api.serializers.serializer_weather_place import WeatherSerializer

class WeatherPlaceViewSet(viewsets.ModelViewSet):
    queryset = GFSForecast.objects.all()
    serializer_class = WeatherSerializer

# Ensure that `DynamicWeatherView` is also defined here
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import logging
from geography.models import Place  # Ensure correct imports

logger = logging.getLogger(__name__)

class DynamicWeatherView(APIView):
    def get_place_details(self, continent, country, region, subregion, city):
        try:
            place = Place.objects.get(
                name=city,
                admin_division__slug=subregion,
                admin_division__parent__slug=region,
                admin_division__parent__parent__slug=country,
                admin_division__parent__parent__parent__slug=continent
            )
            logger.debug(f"Place found: {place}")
            return place.latitude, place.longitude
        except Place.DoesNotExist:
            logger.debug(f"Place not found for: city={city}, subregion={subregion}, region={region}, country={country}, continent={continent}")
            return None, None
        except Exception as e:
            logger.error(f"An error occurred while fetching place details: {e}")
            return None, None

    def get(self, request, continent, country, region, subregion, city):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            latitude, longitude = self.get_place_details(continent, country, region, subregion, city)
            if not latitude or not longitude:
                return Response({"error": "Latitude and longitude are required parameters, or valid place details must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response({"error": "Invalid latitude or longitude."}, status=status.HTTP_400_BAD_REQUEST)

        point = Point(longitude, latitude, srid=4326)

        nearest_forecast = GFSForecast.objects.annotate(distance=Distance('location', point)).order_by('distance').first()

        if not nearest_forecast:
            logger.debug(f"No weather data found for nearest location: ({latitude}, {longitude})")
            return Response({"error": "Weather data not found for the nearest location."}, status=status.HTTP_404_NOT_FOUND)

        forecasts = GFSForecast.objects.filter(latitude=nearest_forecast.latitude, longitude=nearest_forecast.longitude).order_by('timestamp')

        serializer = WeatherSerializer(forecasts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
