"""
This module contains utility functions for geographic operations.
"""

import requests
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from requests.exceptions import RequestException

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

def get_elevation(latitude, longitude):
    """
    Get the elevation of a given latitude and longitude using Google Maps Elevation API.
    """
    api_key = settings.GOOGLE_MAPS_ELEVATION_API_KEY
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={api_key}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        elevation = data['results'][0].get('elevation')
        return elevation

    return None

def get_location_name(latitude, longitude):
    """
    Get the location name and municipality for a given latitude and longitude using OpenCage API.
    """
    api_key = settings.OPENCAGE_API_KEY
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={api_key}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"Request failed: {e}")
        return None, None

    data = response.json()
    if not data['results']:
        return None, None

    result = data['results'][0]
    formatted_name = result.get('formatted')
    components = result.get('components', {})

    municipality = components.get('municipality')

    return formatted_name, municipality
