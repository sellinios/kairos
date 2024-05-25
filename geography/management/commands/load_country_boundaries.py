import os
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from geography.models import Country, Continent

class Command(BaseCommand):
    help = 'Load country boundaries and continents into the database'

    def handle(self, *args, **options):
        shp_file_path = '/home/lefteris.broker/kairos/Data/natural_earth_vector/natural-earth-vector-5.1.0/110m_cultural/ne_110m_admin_0_countries.shp'

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

                # Validate iso_alpha2 length
                if len(iso_alpha2) > 2:
                    self.stdout.write(self.style.ERROR(f"ISO_A2 value too long: {iso_alpha2}"))
                    continue

                # Get or create the continent
                continent, created = Continent.objects.get_or_create(name=continent_name)

                # Get or create the country
                country, created = Country.objects.get_or_create(
                    iso_alpha3=iso_alpha3,
                    defaults={
                        'name': name,
                        'iso_alpha2': iso_alpha2,
                        'iso_numeric': feature.get('ISO_N3'),
                        'continent': continent,
                        'geom': geom
                    }
                )

                if not created:
                    # Update the existing country with new data if necessary
                    country.name = name
                    country.iso_alpha2 = iso_alpha2
                    country.iso_numeric = feature.get('ISO_N3')
                    country.continent = continent
                    country.geom = geom
                    country.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded country boundaries and continents'))
