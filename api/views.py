from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from geography.models import Country, AdministrativeDivision, GeographicEntity, Place
from weather.models import GFSForecast, MetarData
from .serializers import (
    CountrySerializer,
    AdministrativeDivisionSerializer,
    GeographicEntitySerializer,
    PlaceSerializer,
    GFSForecastSerializer,
    MetarDataSerializer
)
from geography.utils import get_location_name

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class AdministrativeDivisionViewSet(viewsets.ModelViewSet):
    queryset = AdministrativeDivision.objects.all()
    serializer_class = AdministrativeDivisionSerializer

class GeographicEntityViewSet(viewsets.ModelViewSet):
    queryset = GeographicEntity.objects.all()
    serializer_class = GeographicEntitySerializer

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest_place(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return Response({"error": "Latitude and longitude are required"}, status=400)

        nearest_place = Place.objects.nearest_place(float(latitude), float(longitude))

        if nearest_place:
            serializer = self.get_serializer(nearest_place)
            return Response(serializer.data)
        else:
            formatted_name, locality = get_location_name(float(latitude), float(longitude))
            if locality:
                geographic_entity, created = GeographicEntity.objects.get_or_create(
                    name=locality,
                    defaults={'entity_type': 'locality'}
                )
                place, place_created = Place.objects.get_or_create(
                    entity=geographic_entity,
                    location=f'POINT({longitude} {latitude})'
                )
                serializer = self.get_serializer(place)
                return Response(serializer.data, status=201)
            else:
                return Response({"error": "Unable to determine locality"}, status=404)

    @action(detail=False, methods=['get'], url_path='entity-name')
    def get_entity_name(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return Response({"error": "Latitude and longitude are required"}, status=400)

        formatted_name, locality = get_location_name(float(latitude), float(longitude))

        if locality:
            geographic_entity, created = GeographicEntity.objects.get_or_create(
                name=locality,
                defaults={'entity_type': 'locality'}
            )
            place, place_created = Place.objects.get_or_create(
                entity=geographic_entity,
                location=f'POINT({longitude} {latitude})'
            )
            place_serializer = PlaceSerializer(place)
            return Response({
                "entity_name": locality,
                "entity_created": created,
                "place_created": place_created,
                "place": place_serializer.data
            })
        else:
            return Response({"error": "No nearby place found"}, status=404)

class GFSForecastViewSet(viewsets.ModelViewSet):
    queryset = GFSForecast.objects.all()
    serializer_class = GFSForecastSerializer

class MetarDataViewSet(viewsets.ModelViewSet):
    queryset = MetarData.objects.all()
    serializer_class = MetarDataSerializer
