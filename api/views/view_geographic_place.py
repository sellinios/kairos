from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geography.models import Place
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

        nearest_place = Place.objects.annotate(distance=Distance('location', user_location)).order_by(
            'distance').first()

        if nearest_place:
            serializer = PlaceSerializer(nearest_place)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No place found'}, status=status.HTTP_404_NOT_FOUND)
