# geography/management/commands/import_greek_regions.py

from django.core.management.base import BaseCommand
from geography.models import GeographicDivision, GeographicLevel, GeographicCountry
import osgeo.ogr as ogr
import os
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Import Greek regions from Natural Earth dataset using English names'

    def handle(self, *args, **kwargs):
        # Path to your Natural Earth shapefile
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.join(base_dir, '../../../')
        shapefile_path = os.path.join(project_dir,
                                      'data/natural-earth-vector-5.1.0/10m_cultural/ne_10m_admin_1_states_provinces.shp')

        # Ensure GeographicCountry and GeographicLevel exist
        country, created = GeographicCountry.objects.get_or_create(name='Greece', defaults={'slug': 'greece'})
        level, created = GeographicLevel.objects.get_or_create(name='Region', level_order=1, country=country)

        # Open the shapefile
        ds = ogr.Open(shapefile_path)
        if ds is None:
            self.stderr.write(self.style.ERROR('Could not open shapefile'))
            return

        layer = ds.GetLayer()
        greek_regions_count = 0

        for feature in layer:
            name = feature.GetField('name_en')  # Ensure to use the English name field
            iso_a2 = feature.GetField('iso_a2')

            # Filter only Greek regions
            if iso_a2 != 'GR':
                continue

            # Get centroid if geometry is not a point
            geom = feature.GetGeometryRef()
            if geom is None:
                self.stdout.write(self.style.WARNING(f'No geometry for {name}, skipping.'))
                continue

            if geom.GetGeometryType() != ogr.wkbPoint:
                geom = geom.Centroid()

            longitude = geom.GetX()
            latitude = geom.GetY()

            # Create or get the geographic division for the region
            division, created = GeographicDivision.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'level': level,
                    'country': country,
                    'parent': None  # Assuming top-level regions have no parent
                }
            )

            greek_regions_count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {name}'))

        ds = None
        self.stdout.write(self.style.SUCCESS(f'Total Greek regions imported: {greek_regions_count}'))
