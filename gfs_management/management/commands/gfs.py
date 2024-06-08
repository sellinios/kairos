import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Execute GFS data download, combine, cleanup temporary files, and cleanup old data in sequence'

    def handle(self, *args, **options):
        commands = [
            'gfs_data_download',
            'gfs_data_combine',
            'gfs_data_cleanup_tmp',
            'gfs_data_cleanup'
        ]

        for command in commands:
            logger.info(f"Running command: {command}")
            try:
                call_command(command)
                logger.info(f"Command {command} completed successfully")
            except Exception as e:
                logger.error(f"Command {command} failed: {e}")
                break

        logger.info("All GFS data processes completed.")
