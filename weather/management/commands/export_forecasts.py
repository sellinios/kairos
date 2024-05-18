import logging
import pandas as pd
from django.core.management.base import BaseCommand
from weather.models import GFSForecast  # Adjust the import to match your actual app and model

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Export forecast data to a CSV file'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Exporting forecasts...'))

        # Fetch data from the database
        forecasts = GFSForecast.objects.all().values()
        if not forecasts.exists():
            self.stdout.write(self.style.WARNING('No forecast data found to export.'))
            logging.warning("No forecast data found to export.")
            return

        df = pd.DataFrame(list(forecasts))

        if df.empty:
            self.stdout.write(self.style.WARNING('No forecast data to export.'))
            logging.warning("No forecast data to export.")
            return

        # Save to CSV
        df.to_csv('GFS/forecasts.csv', index=False)
        logging.info("Forecasts exported successfully.")

        self.stdout.write(self.style.SUCCESS('Forecasts exported successfully.'))
