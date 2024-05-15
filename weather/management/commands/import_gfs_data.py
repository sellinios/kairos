import os
import pandas as pd
from django.core.management.base import BaseCommand
from weather.models import GFSForecast
from geography.models import Place

class Command(BaseCommand):
    help = 'Import extracted GFS data to database'

    def handle(self, *args, **kwargs):
        extracted_dir = './extracted_files'

        place = Place.objects.first()
        if not place:
            self.stderr.write('No place found in the database. Please add a place first.')
            return

        for file_name in os.listdir(extracted_dir):
            if file_name.endswith('.csv'):
                file_path = os.path.join(extracted_dir, file_name)
                self.stdout.write(f'Processing {file_path}...')
                df = pd.read_csv(file_path)

                for _, row in df.iterrows():
                    timestamp = pd.to_datetime(row['valid_time'])
                    temperature = row.get('TMP:2 m above ground', None)
                    precipitation = row.get('APCP:surface', None)
                    wind_speed = row.get('WIND:10 m above ground', None)

                    GFSForecast.objects.create(
                        place=place,
                        temperature=temperature,
                        precipitation=precipitation,
                        wind_speed=wind_speed,
                        timestamp=timestamp
                    )

        self.stdout.write(self.style.SUCCESS('Completed importing GFS data to database.'))
