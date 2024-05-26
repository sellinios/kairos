import requests
from django.conf import settings
from requests.exceptions import RequestException

def get_location_name(latitude, longitude):
    api_key = settings.OPENCAGE_API_KEY
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
    except RequestException as e:
        print(f"Request failed: {e}")
        return None, None

    data = response.json()
    if not data['results']:
        return None, None

    result = data['results'][0]
    formatted_name = result.get('formatted')
    components = result.get('components', {})

    # Extract municipality
    municipality = components.get('municipality')

    return formatted_name, municipality