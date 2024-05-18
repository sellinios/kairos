import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from weather.models import GFSForecast

class Command(BaseCommand):
    help = "Import forecasts from CSV into the database"

    def handle(self, *args, **kwargs):
        input_csv = 'GFS/forecasts.csv'
        try:
            with open(input_csv, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Convert timestamp to aware datetime
                    timestamp = parse_datetime(row['timestamp'])
                    if timestamp is not None and is_naive(timestamp):
                        timestamp = make_aware(timestamp)

                    # Convert numeric fields to appropriate types, handle empty strings
                    temperature = float(row['temperature']) if row['temperature'] else None
                    specific_humidity = float(row['specific_humidity']) if row['specific_humidity'] else None
                    dew_point = float(row['dew_point']) if row['dew_point'] else None
                    relative_humidity = float(row['relative_humidity']) if row['relative_humidity'] else None
                    wind_speed = float(row['wind_speed']) if row['wind_speed'] else None
                    precipitation = float(row['precipitation']) if row['precipitation'] else None
                    apparent_temperature = float(row['apparent_temperature']) if row['apparent_temperature'] else None

                    GFSForecast.objects.update_or_create(
                        place_id=row['place_id'],
                        timestamp=timestamp,
                        defaults={
                            'temperature': temperature,
                            'specific_humidity': specific_humidity,
                            'dew_point': dew_point,
                            'relative_humidity': relative_humidity,
                            'wind_speed': wind_speed,
                            'precipitation': precipitation,
                            'apparent_temperature': apparent_temperature,
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported forecasts from CSV'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing forecasts from CSV: {e}'))
