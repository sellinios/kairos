import logging
import pandas as pd
from django.core.management.base import BaseCommand
from weather.models import GFSForecast
from geography.models import Place
from datetime import timedelta
import pytz

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Import forecast data from consolidated_forecasts.csv file'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Importing forecasts...'))

        try:
            # Read the places.csv file
            places_df = pd.read_csv('GFS/places.csv')
            places_df['lat_lon_key'] = places_df.apply(lambda row: (round(row['latitude'], 1), round(row['longitude'], 1)), axis=1)

            # Create a dictionary to quickly lookup place_id by rounded latitude and longitude
            places_dict = places_df.set_index('lat_lon_key')['place_id'].to_dict()

            # Define expected columns for the forecast CSV
            forecast_columns = ['latitude', 'longitude', 'time', 'step', 'surface', 'valid_time', 'tp', 'forecast_time', 'variable', 'acpcp', 'watr']

            # Process the CSV file in chunks to handle large files efficiently
            chunksize = 1000
            for chunk in pd.read_csv('GFS/consolidated_forecasts.csv', chunksize=chunksize, names=forecast_columns, header=0):
                if chunk.empty:
                    self.stdout.write(self.style.WARNING('The forecast file is empty. No data to import.'))
                    logging.warning("The forecast file is empty. No data to import.")
                    return

                # Insert data into the database
                for _, row in chunk.iterrows():
                    lat_lon_key = (round(row['latitude'], 1), round(row['longitude'], 1))
                    place_id = places_dict.get(lat_lon_key)

                    if place_id:  # Only import data if a nearby place is found
                        # Make datetime fields timezone-aware
                        valid_time = pd.to_datetime(row['valid_time']).tz_localize(pytz.UTC)
                        forecast_time = pd.to_datetime(row['forecast_time']).tz_localize(pytz.UTC)
                        time = pd.to_datetime(row['time']).tz_localize(pytz.UTC)

                        GFSForecast.objects.update_or_create(
                            place_id=place_id,
                            valid_time=valid_time,
                            defaults={
                                'time': time,
                                'step': pd.to_timedelta(row['step']),  # Convert the step to a timedelta
                                'surface': row['surface'],
                                'tp': row['tp'],
                                'forecast_time': forecast_time,
                                'variable': row['variable'],
                                'acpcp': row['acpcp'],
                                'watr': row['watr'],
                            }
                        )

            logging.info("Forecasts imported successfully.")
            self.stdout.write(self.style.SUCCESS('Forecasts imported successfully.'))

        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('No columns to parse from file. The forecast file may be empty or corrupted.'))
            logging.error("No columns to parse from file. The forecast file may be empty or corrupted.")

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Forecast file not found. Please ensure GFS/consolidated_forecasts.csv exists.'))
            logging.error("Forecast file not found. Please ensure GFS/consolidated_forecasts.csv exists.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing forecast data: {e}'))
            logging.error(f"Error importing forecast data: {e}")
