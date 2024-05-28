from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from geography.models import Place
from weather.models import GFSForecast  # Adjust the import based on your actual model
from api.serializers.serializer_weather_place import WeatherSerializer, PlaceSerializer  # Import the serializers
from rest_framework import status

class WeatherPlaceViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for retrieving weather information for a specific place.
    """

    @action(detail=False, methods=['get'], url_path='weather/europe/greece/attica/(?P<municipality>[^/.]+)/(?P<place_slug>[^/.]+)')
    def retrieve_weather(self, request, municipality=None, place_slug=None):
        try:
            place = Place.objects.get(slug=place_slug, admin_division__slug=municipality)
            weather_data = GFSForecast.objects.filter(place=place)  # Adjust the filtering as per your actual model relations
            place_serializer = PlaceSerializer(place)
            weather_serializer = WeatherSerializer(weather_data, many=True)
            return Response({
                'place': place_serializer.data,
                'weather_data': weather_serializer.data,
                'full_url': place.get_full_url(),
                'weather_url': place.get_weather_url()
            })
        except Place.DoesNotExist:
            return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)
