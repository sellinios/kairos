import requests
from django.conf import settings
from requests.exceptions import RequestException
from geography.models.model_geographic_place import Place
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

def get_location_name(latitude, longitude):
    api_key = settings.OPENCAGE_API_KEY
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={api_key}'

    try:
        response = requests.get(url)
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

nearest_place_cache = {}

def find_nearest_place(latitude, longitude):
    point = Point(longitude, latitude, srid=4326)
    location_key = (latitude, longitude)

    if location_key in nearest_place_cache:
        return nearest_place_cache[location_key]

    nearest_place = Place.objects.annotate(distance=Distance('location', point)).order_by('distance').first()
    nearest_place_cache[location_key] = nearest_place

    return nearest_place
