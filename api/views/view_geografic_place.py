from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from geography.models import Place, AdminDivisionInstance, Category, Level
from api.serializers.serializer_geografic_place import PlaceSerializer
from geography.utils import get_location_name

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
                municipality_level, created = Level.objects.get_or_create(name='Municipality')

                admin_division, created = AdminDivisionInstance.objects.get_or_create(
                    name=locality,
                    defaults={'level': municipality_level}
                )

                default_category, created = Category.objects.get_or_create(name='default')

                place, place_created = Place.objects.get_or_create(
                    longitude=float(longitude),
                    latitude=float(latitude),
                    defaults={'admin_division': admin_division, 'category': default_category}
                )

                serializer = self.get_serializer(place)
                return Response(serializer.data, status=201 if place_created else 200)
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
            municipality_level, created = Level.objects.get_or_create(name='Municipality')

            admin_division, created = AdminDivisionInstance.objects.get_or_create(
                name=locality,
                defaults={'level': municipality_level}
            )

            default_category, created = Category.objects.get_or_create(name='default')

            place, place_created = Place.objects.get_or_create(
                longitude=float(longitude),
                latitude=float(latitude),
                defaults={'admin_division': admin_division, 'category': default_category}
            )

            place_serializer = PlaceSerializer(place)
            return Response({
                "entity_name": locality,
                "place_created": place_created,
                "place": place_serializer.data
            })
        else:
            return Response({"error": "No nearby place found"}, status=404)
