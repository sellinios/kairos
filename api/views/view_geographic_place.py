from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from geography.models.model_geographic_place import Place
from geography.models.model_geographic_admin_division import AdminDivisionInstance
from geography.models.model_geographic_category import Category
from geography.models.model_geographic_level import Level
from api.serializers.serializer_geografic_place import PlaceSerializer
from geography.utils import get_location_name, find_nearest_place

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest_place(self, request):
        from django.http import JsonResponse  # Local import to avoid circular import

        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return JsonResponse({"error": "Latitude and longitude are required"}, status=400)

        nearest_place = find_nearest_place(float(latitude), float(longitude))

        if nearest_place:
            serializer = self.get_serializer(nearest_place)
            return Response(serializer.data)
        else:
            return self._create_or_fetch_place(float(latitude), float(longitude))

    @action(detail=False, methods=['get'], url_path='entity-name')
    def get_entity_name(self, request):
        from django.http import JsonResponse  # Local import to avoid circular import

        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return JsonResponse({"error": "Latitude and longitude are required"}, status=400)

        return self._create_or_fetch_place(float(latitude), float(longitude))

    def _create_or_fetch_place(self, latitude, longitude):
        from django.http import JsonResponse  # Local import to avoid circular import

        formatted_name, locality = get_location_name(latitude, longitude)

        if locality:
            municipality_level, created = Level.objects.get_or_create(name='Municipality')

            admin_division, created = AdminDivisionInstance.objects.get_or_create(
                name=locality,
                defaults={'level': municipality_level}
            )

            default_category, created = Category.objects.get_or_create(name='default')

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
            return JsonResponse({"error": "No nearby place found"}, status=404)
