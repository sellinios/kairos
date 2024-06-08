import os
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from gfs_management.models import GFSParameter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_parameters_from_file(file_path):
    parameters = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Skip the header line
            for line in lines[1:]:
                cols = line.strip().split('\t')
                if len(cols) == 5:
                    level_layer = cols[1]
                    parameter = cols[2]
                    forecast_valid = cols[3]
                    description = cols[4]
                    parameters.append({
                        "level_layer": level_layer,
                        "parameter": parameter,
                        "forecast_valid": forecast_valid,
                        "description": description
                    })
                else:
                    logger.warning(f"Skipping row with incorrect columns: {line}")
    except Exception as e:
        logger.error(f"Error reading parameters file: {e}")

    logger.info(f"Read {len(parameters)} parameters from the file.")
    return parameters

def import_parameters_to_db(parameters):
    for idx, param in enumerate(parameters, start=1):
        try:
            GFSParameter.objects.update_or_create(
                number=idx,
                defaults={
                    'level_layer': param["level_layer"],
                    'parameter': param["parameter"],
                    'forecast_valid': param["forecast_valid"],
                    'description': param["description"],
                    'last_updated': timezone.now()
                }
            )
            logger.info(f"Imported parameter: {param['parameter']} (Level: {param['level_layer']}, Number: {idx})")
        except Exception as e:
            logger.error(f"Error importing parameter {param['parameter']}: {e}")

class Command(BaseCommand):
    help = 'Import GFS parameters from a text file into the database'

    def handle(self, *args, **options):
        logger.info("Starting the import of GFS parameters from the text file.")

        file_path = "data/parameters.txt"
        if not os.path.exists(file_path):
            logger.error(f"Parameters file not found: {file_path}")
            return

        parameters = read_parameters_from_file(file_path)
        if parameters:
            import_parameters_to_db(parameters)
            logger.info("GFS parameters import process completed.")
        else:
            logger.error("No parameters were read from the file.")
