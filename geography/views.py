from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Country, Region, RegionalUnit, Municipality, Place
from .serializers import CountrySerializer, RegionSerializer, RegionalUnitSerializer, MunicipalitySerializer, PlaceSerializer
from weather.models import GFSForecast
from weather.serializers import GFSForecastSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionalUnitViewSet(viewsets.ModelViewSet):
    queryset = RegionalUnit.objects.all()
    serializer_class = RegionalUnitSerializer

class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(detail=True, methods=['get'], url_path='forecast')
    def get_forecast(self, request, pk=None):
        place = self.get_object()
        forecasts = GFSForecast.objects.filter(place=place).order_by('timestamp')
        serializer = GFSForecastSerializer(forecasts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest_place(self, request):
        """Retrieve the nearest place based on latitude and longitude."""
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            place = Place.objects.nearest_place(latitude, longitude)
            if place:
                serializer = self.get_serializer(place)
                return Response(serializer.data)
            else:
                return Response({"message": "No nearby place found"}, status=404)
        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid latitude or longitude values provided"}, status=400)
