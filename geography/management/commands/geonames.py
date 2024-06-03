import requests
from django.core.management.base import BaseCommand
from geography.models import GeographicDivision, GeographicLevel, GeographicCountry, GeographicPlace
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import Greek regions, municipalities, and places from Geonames'

    def handle(self, *args, **kwargs):
        # Ensure GeographicCountry and GeographicLevel exist
        country, created = GeographicCountry.objects.get_or_create(name='Greece', defaults={'slug': 'greece'})
        region_level, created = GeographicLevel.objects.get_or_create(name='Region', level_order=1, country=country)
        municipality_level, created = GeographicLevel.objects.get_or_create(name='Municipality', level_order=2, country=country)

        # Geonames URL to fetch regions data
        regions_url = "http://api.geonames.org/childrenJSON?geonameId=390903&username=sellinios"
        response = requests.get(regions_url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch regions data'))
            return

        regions_data = response.json()
        for region in regions_data.get('geonames', []):
            region_name = region['name']
            region_slug = self.get_unique_slug(region_name, None, region_level, country)

            region_obj, created = GeographicDivision.objects.get_or_create(
                name=region_name,
                level=region_level,
                country=country,
                defaults={'slug': region_slug, 'parent': None}
            )
            self.stdout.write(self.style.SUCCESS(f'Imported region: {region_name}'))

            municipalities_url = f"http://api.geonames.org/childrenJSON?geonameId={region['geonameId']}&username=sellinios"
            municipalities_response = requests.get(municipalities_url)
            if municipalities_response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'Failed to fetch municipalities data for {region_name}'))
                continue

            municipalities_data = municipalities_response.json()
            for municipality in municipalities_data.get('geonames', []):
                fcode = municipality['fcode']
                name = municipality['name']
                self.stdout.write(self.style.SUCCESS(f'Found municipality candidate: {name} with fcode: {fcode}'))

                if fcode in ['ADM2', 'ADM3']:
                    municipality_name = name
                    municipality_slug = self.get_unique_slug(municipality_name, region_obj, municipality_level, country)

                    municipality_obj, created = GeographicDivision.objects.get_or_create(
                        name=municipality_name,
                        level=municipality_level,
                        country=country,
                        parent=region_obj,
                        defaults={'slug': municipality_slug}
                    )
                    self.stdout.write(self.style.SUCCESS(f'Imported municipality: {municipality_name}'))

                    # Fetch places within the municipality
                    places_url = f"http://api.geonames.org/childrenJSON?geonameId={municipality['geonameId']}&username=sellinios"
                    places_response = requests.get(places_url)
                    if places_response.status_code != 200:
                        self.stdout.write(self.style.ERROR(f'Failed to fetch places data for {municipality_name}'))
                        continue

                    places_data = places_response.json()
                    for place in places_data.get('geonames', []):
                        place_name = place['name']
                        latitude = place['lat']
                        longitude = place['lng']
                        place_slug = self.get_unique_slug(place_name, municipality_obj, None, country)

                        place_obj, created = GeographicPlace.objects.get_or_create(
                            name=place_name,
                            admin_division=municipality_obj,
                            defaults={
                                'slug': place_slug,
                                'latitude': latitude,
                                'longitude': longitude,
                                'location': f'POINT({longitude} {latitude})'
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'Imported place: {place_name}'))

        self.stdout.write(self.style.SUCCESS('Import process completed.'))

    def get_unique_slug(self, name, parent, level, country):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        if level:
            while GeographicDivision.objects.filter(slug=slug, level=level, country=country, parent=parent).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        else:
            while GeographicPlace.objects.filter(slug=slug, admin_division=parent).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug
