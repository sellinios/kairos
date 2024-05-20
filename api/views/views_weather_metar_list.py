from rest_framework.views import APIView
from rest_framework.response import Response
from weather.models import MetarData
from ..serializers import MetarDataSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

class MetarListView(APIView):
    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude is None or longitude is None:
            return Response({'error': 'Latitude and longitude parameters are required.'}, status=400)

        try:
            current_location = Point(float(longitude), float(latitude), srid=4326)
            metar_data = MetarData.objects.filter(
                station__location__distance_lte=(current_location, 10000)  # 10km radius
            ).annotate(
                distance=Distance('station__location', current_location)
            ).order_by('distance', '-metar_timestamp')[:1]

            if not metar_data.exists():
                return Response({'error': 'No METAR data found for the given coordinates'}, status=404)

            serializer = MetarDataSerializer(metar_data, many=True)
            return Response(serializer.data)
        except MetarData.DoesNotExist:
            return Response({'error': 'No METAR data found for the given coordinates'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
