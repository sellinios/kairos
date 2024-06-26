import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Execute GFS data download, combine, parse, cleanup temporary files, and cleanup old data in sequence'

    def handle(self, *args, **options):
        """Handles the execution of a sequence of GFS data-related commands."""

        commands = [
            'gfs_data_download',
            'gfs_data_filtered',
            'gfs_data_import',  # Add the new parsing step
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
                # Optional: Continue with the next command instead of breaking
                # continue
                break

        logger.info("All GFS data processes completed.")
