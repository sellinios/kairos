# geography/geographic_utils.py

import requests
from django.conf import settings
from requests.exceptions import RequestException

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
    Get the location name for a given latitude and longitude using Google Geocoding API.
    """
    api_key = settings.GOOGLE_MAPS_GEOCODING_API_KEY
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"Request failed: {e}")
        return "Unknown"

    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        address_components = data['results'][0]['address_components']
        formatted_address = data['results'][0]['formatted_address']
        for component in address_components:
            if 'locality' in component['types']:
                locality = component['long_name']
                return locality
        return formatted_address
    else:
        return "Unknown"
