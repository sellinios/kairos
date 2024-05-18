import pandas as pd
import logging
from django.core.management.base import BaseCommand
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Read and display the content of places.csv from GFS folder'

    def handle(self, *args, **kwargs):
        try:
            # Define the path to the places.csv file in the GFS folder
            file_path = os.path.join('GFS', 'places.csv')

            # Read the places.csv file
            places_df = pd.read_csv(file_path)

            # Display the header and first 10 rows
            logging.info(f"Header and first 10 lines of places.csv:\n{places_df.head(10)}")

            self.stdout.write(self.style.SUCCESS(f"Header and first 10 lines of places.csv:\n{places_df.head(10)}"))

        except FileNotFoundError:
            logging.error("places.csv file not found in the GFS folder. Please ensure the file exists.")
            self.stdout.write(self.style.ERROR("places.csv file not found in the GFS folder. Please ensure the file exists."))

        except pd.errors.EmptyDataError:
            logging.error("places.csv file is empty or corrupted.")
            self.stdout.write(self.style.ERROR("places.csv file is empty or corrupted."))

        except Exception as e:
            logging.error(f"Error reading places.csv: {e}")
            self.stdout.write(self.style.ERROR(f"Error reading places.csv: {e}"))
