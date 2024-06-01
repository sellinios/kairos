# weather/management/commands/update_gfs.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update GFS data by calling the gfs command'

    def handle(self, *args, **kwargs):
        logger.info("Starting the update_gfs command.")
        try:
            call_command('gfs')
            logger.info("Successfully updated GFS data.")
        except Exception as e:
            logger.error("Error while updating GFS data: %s", e)
            self.stdout.write(self.style.ERROR(f'Error updating GFS data: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully updated GFS data'))
