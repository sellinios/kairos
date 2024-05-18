import logging
import pandas as pd
from django.core.management.base import BaseCommand

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Command(BaseCommand):
    help = 'Read and display the header and first 10 lines of consolidated_forecasts.csv'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Reading consolidated_forecasts.csv...'))

        try:
            # Read the CSV file in chunks
            chunksize = 10
            chunk_iter = pd.read_csv('GFS/consolidated_forecasts.csv', chunksize=chunksize)
            first_chunk = next(chunk_iter)

            if first_chunk.empty:
                self.stdout.write(self.style.WARNING('The consolidated forecasts file is empty.'))
                logging.warning("The consolidated forecasts file is empty.")
                return

            # Display the header and first 10 lines
            self.stdout.write(self.style.SUCCESS('Header and first 10 lines of consolidated_forecasts.csv:'))
            self.stdout.write(first_chunk.to_string(index=False))
            logging.info("Displayed the header and first 10 lines of consolidated_forecasts.csv.")

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('consolidated_forecasts.csv file not found. Please ensure the file exists.'))
            logging.error("consolidated_forecasts.csv file not found. Please ensure the file exists.")

        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('No columns to parse from file. The file may be empty or corrupted.'))
            logging.error("No columns to parse from file. The file may be empty or corrupted.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading consolidated_forecasts.csv: {e}'))
            logging.error(f"Error reading consolidated_forecasts.csv: {e}")
