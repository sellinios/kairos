import logging
from django.core.management import BaseCommand, call_command

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Central command for managing GFS-related tasks'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Running export_places...'))
        call_command('export_places')  # Step 1: Export geographical data

        self.stdout.write(self.style.SUCCESS('Running consolidate_data...'))
        call_command('consolidate_data')  # Step 2: Consolidate data from various sources

        self.stdout.write(self.style.SUCCESS('Running export_forecasts...'))
        call_command('export_forecasts')  # Step 3: Export the consolidated forecast data

        self.stdout.write(self.style.SUCCESS('Running import_forecasts...'))
        call_command('import_forecasts')  # Step 4: Import external forecast data

        self.stdout.write(self.style.SUCCESS('All tasks completed successfully.'))
