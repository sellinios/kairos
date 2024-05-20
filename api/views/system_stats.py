from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import Country, AdministrativeDivision, GeographicEntity, Place

@api_view(['GET'])
def get_system_stats(request):
    country_count = Country.objects.count()
    administrative_division_count = AdministrativeDivision.objects.count()
    geographic_entity_count = GeographicEntity.objects.count()
    place_count = Place.objects.count()

    return Response({
        'countries': country_count,
        'administrative_divisions': administrative_division_count,
        'geographic_entities': geographic_entity_count,
        'places': place_count
    })
