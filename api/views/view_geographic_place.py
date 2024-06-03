# api/views/view_geographic_place.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models import GeographicPlace, GeographicDivision, GeographicCountry, GeographicContinent
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

        nearest_place = GeographicPlace.objects.annotate(distance=Distance('location', user_location)).order_by('distance').first()

        if nearest_place:
            data = PlaceSerializer(nearest_place).data
            # Adding hierarchy data
            division = nearest_place.admin_division
            data['subregion'] = division.slug
            data['region'] = division.parent.slug if division.parent else 'unknown'
            data['country'] = division.country.slug if division.country else 'unknown'
            data['continent'] = division.country.continent.slug if division.country and division.country.continent else 'unknown'
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No place found'}, status=status.HTTP_404_NOT_FOUND)
