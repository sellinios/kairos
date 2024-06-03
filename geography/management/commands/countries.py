import os
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from geography.models import GeographicCountry, GeographicContinent

class Command(BaseCommand):
    help = 'Load country boundaries and continents into the database'

    def handle(self, *args, **options):
        shp_file_path = '/home/lefteris.broker/aethra/data/natural-earth-vector-5.1.0/10m_cultural/ne_10m_admin_0_countries.shp'

        if not os.path.exists(shp_file_path):
            self.stdout.write(self.style.ERROR(f"Shapefile not found: {shp_file_path}"))
            return

        try:
            ds = DataSource(shp_file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading shapefile: {e}"))
            return

        for layer in ds:
            for feature in layer:
                iso_alpha3 = feature.get('ISO_A3')
                name = feature.get('NAME')
                continent_name = feature.get('CONTINENT')
                geom = feature.geom.geos

                # Convert Polygon to MultiPolygon if necessary
                if isinstance(geom, Polygon):
                    geom = MultiPolygon(geom)

                iso_alpha2 = feature.get('ISO_A2')

                # Debugging: Print values and their lengths
                print(f"ISO_A2: {iso_alpha2} (length: {len(iso_alpha2)})")
                print(f"ISO_A3: {iso_alpha3} (length: {len(iso_alpha3)})")

                # Validate iso_alpha2 and iso_alpha3 length
                if not iso_alpha2 or len(iso_alpha2) != 2 or iso_alpha2 == '-99':
                    self.stdout.write(self.style.ERROR(f"ISO_A2 value invalid or too long: {iso_alpha2}"))
                    continue  # Skip this record

                if not iso_alpha3 or len(iso_alpha3) != 3 or iso_alpha3 == '-99':
                    self.stdout.write(self.style.ERROR(f"ISO_A3 value invalid or too long: {iso_alpha3}"))
                    continue  # Skip this record

                # Get or create the continent
                continent, created = GeographicContinent.objects.get_or_create(name=continent_name)

                # Handle missing fields by checking if they exist in the feature
                area = feature.get('AREA') if 'AREA' in feature.fields else None
                capital = feature.get('CAPITAL') if 'CAPITAL' in feature.fields else None
                official_languages = feature.get('LANGUAGES') if 'LANGUAGES' in feature.fields else None
                currency = feature.get('CURRENCY') if 'CURRENCY' in feature.fields else None
                iso_numeric = feature.get('ISO_N3') if 'ISO_N3' in feature.fields else None

                # Update or create the country
                GeographicCountry.objects.update_or_create(
                    iso_alpha3=iso_alpha3,
                    defaults={
                        'name': name,
                        'iso_alpha2': iso_alpha2,
                        'iso_numeric': iso_numeric,
                        'continent': continent,
                        'geom': geom,
                        'area': area,
                        'capital': capital,
                        'official_languages': official_languages,
                        'currency': currency
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded country boundaries and continents'))
