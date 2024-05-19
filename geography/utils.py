import requests
from django.conf import settings


def get_location_name(latitude, longitude):
    api_key = settings.OPENCAGE_API_KEY
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            result = data['results'][0]
            formatted_name = result.get('formatted')
            components = result.get('components', {})
            locality = components.get('locality') or components.get('suburb')
            return formatted_name, locality
        else:
            return None, None
    else:
        response.raise_for_status()
