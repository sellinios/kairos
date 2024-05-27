# geography/geographic_utils.py

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

# Cache to store nearest place lookups
nearest_place_cache = {}

def find_nearest_place(latitude, longitude, place_queryset):
    """
    Find the nearest place to the given latitude and longitude.
    """
    point = Point(longitude, latitude, srid=4326)
    location_key = (latitude, longitude)

    if location_key in nearest_place_cache:
        return nearest_place_cache[location_key]

    nearest_place = place_queryset.annotate(distance=Distance('location', point)).order_by('distance').first()
    nearest_place_cache[location_key] = nearest_place

    return nearest_place

def store_new_place(name, latitude, longitude, height=0):
    """
    Store a new Place instance in the database.
    """
    from django.apps import apps
    Place = apps.get_model('geography', 'Place')
    place = Place.objects.create(
        name=name,
        latitude=latitude,
        longitude=longitude,
        height=height,
        location=Point(longitude, latitude, srid=4326)
    )
    return place
