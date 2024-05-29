# api/views/view_weather_places.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from weather.models.model_gfs_forecast import GFSForecast
from api.serializers.serializer_weather_places import GFSForecastSerializer
from geography.models.model_geographic_place import Place
from geography.models.model_geographic_admin_division import AdminDivisionInstance
from geography.models.model_geographic_country import Country
from geography.models.model_geographic_continent import Continent
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

class WeatherDetailAPIView(APIView):
    def get(self, request, continent, country, levels_and_place):
        levels = levels_and_place.split('/')
        place_name = levels[-1]
        admin_division_names = levels[:-1]

        # Get the continent
        continent_obj = get_object_or_404(Continent, slug=continent)

        # Get the country
        country_obj = get_object_or_404(Country, slug=country, continent=continent_obj)

        # Get the admin divisions in the correct order
        admin_division_obj = None
        for division_name in admin_division_names:
            if admin_division_obj:
                admin_division_obj = get_object_or_404(
                    AdminDivisionInstance, slug=division_name, parent=admin_division_obj
                )
            else:
                admin_division_obj = get_object_or_404(
                    AdminDivisionInstance, slug=division_name, country=country_obj
                )

        # Get the place
        place_obj = get_object_or_404(Place, slug=place_name, admin_division=admin_division_obj)

        # Find the nearest GFS forecast point
        location = place_obj.location  # Use 'location' instead of 'boundary'
        nearest_forecast = GFSForecast.objects.annotate(
            distance=Distance('location', location)
        ).order_by('distance').first()  # Get the nearest forecast point

        if not nearest_forecast:
            return Response({'error': 'No forecast data available'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GFSForecastSerializer(nearest_forecast)
        return Response(serializer.data, status=status.HTTP_200_OK)
