from rest_framework import viewsets, status  # Add status here
from rest_framework.decorators import action
from rest_framework.response import Response
from geography.models.model_geographic_place import Place
from geography.models.model_geographic_admin_division import AdminDivisionInstance
from geography.models.model_geographic_category import Category
from geography.models.model_geographic_level import Level
from api.serializers.serializer_geografic_place import PlaceSerializer
from geography.utils import get_location_name, find_nearest_place
import logging

logger = logging.getLogger(__name__)

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest_place(self, request):
        from django.http import JsonResponse  # Local import to avoid circular import

        latitude, longitude = self._get_lat_lon_from_request(request)
        if latitude is None or longitude is None:
            return self._error_response("Latitude and longitude are required")

        nearest_place = find_nearest_place(latitude, longitude)
        if nearest_place:
            serializer = self.get_serializer(nearest_place)
            return Response(serializer.data)
        else:
            return self._create_or_fetch_place(latitude, longitude)

    @action(detail=False, methods=['get'], url_path='entity-name')
    def get_entity_name(self, request):
        from django.http import JsonResponse  # Local import to avoid circular import

        latitude, longitude = self._get_lat_lon_from_request(request)
        if latitude is None or longitude is None:
            return self._error_response("Latitude and longitude are required")

        return self._create_or_fetch_place(latitude, longitude)

    def _create_or_fetch_place(self, latitude, longitude):
        from django.http import JsonResponse  # Local import to avoid circular import

        formatted_name, locality = get_location_name(latitude, longitude)

        if locality:
            municipality_level, _ = Level.objects.get_or_create(name='Municipality')
            admin_division, _ = AdminDivisionInstance.objects.get_or_create(
                name=locality,
                defaults={'level': municipality_level}
            )
            default_category, _ = Category.objects.get_or_create(name='default')
            place, place_created = Place.objects.get_or_create(
                longitude=longitude,
                latitude=latitude,
                defaults={'admin_division': admin_division, 'category': default_category}
            )

            place_serializer = PlaceSerializer(place)
            return Response({
                "entity_name": locality,
                "place_created": place_created,
                "place": place_serializer.data
            })
        else:
            return self._error_response("No nearby place found", status=status.HTTP_404_NOT_FOUND)

    def _get_lat_lon_from_request(self, request):
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            return latitude, longitude
        except (TypeError, ValueError):
            logger.error("Invalid latitude or longitude in request")
            return None, None

    def _error_response(self, message, status=status.HTTP_400_BAD_REQUEST):
        from django.http import JsonResponse  # Local import to avoid circular import
        return JsonResponse({"error": message}, status=status)
