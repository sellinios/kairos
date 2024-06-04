from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from geography.models import GeographicPlace, GeographicCategory, GeographicCountry, GeographicDivision, GeographicLevel


class Command(BaseCommand):
    help = 'Create a GeographicPlace instance for Greece with specified latitude and longitude.'

    def handle(self, *args, **kwargs):
        greece_latitude = 39.0742
        greece_longitude = 21.8243
        default_category = GeographicCategory.objects.first()

        # Ensure that the GeographicCountry for Greece exists
        country = GeographicCountry.objects.filter(name="Greece").first()
        if not country:
            self.stdout.write(self.style.ERROR('GeographicCountry for Greece not found.'))
            return

        # Ensure that the GeographicDivision for Greece exists at the country level
        greece_division = GeographicDivision.objects.filter(name="Greece", level__name="Country").first()
        if not greece_division:
            self.stdout.write(self.style.ERROR('GeographicDivision for Greece at Country level not found.'))
            return

        # Ensure that the default municipality exists
        default_municipality = GeographicDivision.objects.filter(name="Default Municipality",
                                                                 level__name="Municipality").first()
        if not default_municipality:
            self.stdout.write(self.style.ERROR('Default Municipality not found.'))
            return

        place_name = f"Greece {greece_latitude}, {greece_longitude}"
        place_slug = f"{greece_latitude}-{greece_longitude}"

        place, created = GeographicPlace.objects.get_or_create(
            latitude=greece_latitude,
            longitude=greece_longitude,
            defaults={
                'name': place_name,
                'slug': place_slug,
                'category': default_category,
                'admin_division': default_municipality,
                'location': Point(greece_longitude, greece_latitude, srid=4326),
                'elevation': 0,
                'confirmed': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created GeographicPlace: {place_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'GeographicPlace already exists: {place_name}'))
