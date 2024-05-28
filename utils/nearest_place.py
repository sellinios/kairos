from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from geography.models import Place

def find_nearest_place(latitude, longitude, max_distance_km=10):
    point = Point(longitude, latitude, srid=4326)
    nearest_places = Place.objects.annotate(distance=Distance('location', point)).filter(distance__lte=max_distance_km * 1000).order_by('distance')
    return nearest_places.first() if nearest_places.exists() else None
