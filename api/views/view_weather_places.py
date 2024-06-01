from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from weather.models.model_gfs_forecast import GFSForecast
from api.serializers.serializer_weather_places import GFSForecastSerializer
from geography.models.model_geographic_place import GeographicPlace
from geography.models.model_geographic_division import GeographicDivision
from geography.models.model_geographic_country import GeographicCountry
from geography.models.model_geographic_continent import GeographicContinent
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

class WeatherDetailAPIView(APIView):
    def get(self, request, continent, country, levels_and_place):
        levels = levels_and_place.split('/')
        place_name = levels[-1]
        admin_division_names = levels[:-1]

        # Get the continent
        continent_obj = get_object_or_404(GeographicContinent, slug=continent)

        # Get the country
        country_obj = get_object_or_404(GeographicCountry, slug=country, continent=continent_obj)

        # Get the admin divisions in the correct order
        admin_division_obj = None
        for division_name in admin_division_names:
            if admin_division_obj:
                admin_division_obj = get_object_or_404(
                    GeographicDivision, slug=division_name, parent=admin_division_obj
                )
            else:
                admin_division_obj = get_object_or_404(
                    GeographicDivision, slug=division_name, country=country_obj
                )

        # Get the place
        place_obj = get_object_or_404(GeographicPlace, slug=place_name, admin_division=admin_division_obj)

        # Find the nearest GFS forecast point
        location = place_obj.location
        nearest_forecast_point = GFSForecast.objects.annotate(
            distance=Distance('location', location)
        ).order_by('distance').first()

        if not nearest_forecast_point:
            return Response({'error': 'No forecast data available'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all forecast entries for the nearest forecast point
        nearest_forecasts = GFSForecast.objects.filter(
            latitude=nearest_forecast_point.latitude,
            longitude=nearest_forecast_point.longitude
        ).order_by('timestamp')

        serializer = GFSForecastSerializer(nearest_forecasts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models import GeographicPlace
from api.serializers.serializer_geographic_place import PlaceSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

class NearestPlaceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response({'error': 'Invalid latitude or longitude'}, status=status.HTTP_400_BAD_REQUEST)

        user_location = Point(longitude, latitude, srid=4326)

        nearest_place = GeographicPlace.objects.annotate(distance=Distance('location', user_location)).order_by(
            'distance').first()

        if nearest_place:
            serializer = PlaceSerializer(nearest_place)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No place found'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets
from geography.models import GeographicContinent
from api.serializers.serializer_geographic_continent import ContinentSerializer

class ContinentViewSet(viewsets.ModelViewSet):
    queryset = GeographicContinent.objects.all()
    serializer_class = ContinentSerializer
