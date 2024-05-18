import csv
from django.core.management.base import BaseCommand
from geography.models import Place

class Command(BaseCommand):
    help = "Export places to a CSV file"

    def handle(self, *args, **kwargs):
        places = Place.objects.all()
        with open('GFS/places.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'latitude', 'longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for place in places:
                writer.writerow({'id': place.id, 'name': place.name, 'latitude': place.latitude, 'longitude': place.longitude})

        self.stdout.write(self.style.SUCCESS('Successfully exported places to GFS/places.csv'))
