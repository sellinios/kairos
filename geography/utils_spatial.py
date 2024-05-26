# geography/utils_spatial.py

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from geography.models import Place

# Cache to store nearest place lookups
nearest_place_cache = {}


def find_nearest_place(latitude, longitude):
    point = Point(longitude, latitude, srid=4326)
    location_key = (latitude, longitude)

    if location_key in nearest_place_cache:
        return nearest_place_cache[location_key]

    nearest_place = Place.objects.annotate(distance=Distance('location', point)).order_by('distance').first()
    nearest_place_cache[location_key] = nearest_place

    return nearest_place
