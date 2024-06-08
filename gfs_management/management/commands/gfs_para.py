import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from gfs_management.models import GFSParameter
from django.db import connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_gfs_parameters_from_file(file_path):
    parameters = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Skip the header line
            for line in lines[1:]:
                cols = line.strip().split('\t')
                if len(cols) == 5:
                    param_number = int(cols[0])
                    level_layer = cols[1]
                    parameter = cols[2]
                    forecast_valid = cols[3]
                    description = cols[4]
                    parameters.append({
                        "number": param_number,
                        "level_layer": level_layer,
                        "parameter": parameter,
                        "forecast_valid": forecast_valid,
                        "description": description
                    })
                else:
                    logger.warning(f"Skipping row with incorrect columns: {line}")
    except Exception as e:
        logger.error(f"Error reading parameters file: {e}")

    logger.info(f"Fetched and parsed {len(parameters)} GFS parameters from the file.")
    return parameters

def delete_all_gfs_parameters():
    logger.info("Deleting all existing GFSParameter records.")
    GFSParameter.objects.all().delete()

def reset_gfs_parameter_id_sequence():
    logger.info("Resetting GFSParameter ID sequence.")
    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE gfs_management_gfsparameter_id_seq RESTART WITH 1;")

def import_gfs_parameters(parameters):
    for param in parameters:
        GFSParameter.objects.create(
            number=param["number"],
            level_layer=param["level_layer"],
            parameter=param["parameter"],
            forecast_valid=param["forecast_valid"],
            description=param["description"],
            last_updated=timezone.now()
        )
        logger.info(
            f"Saved GFS parameter: {param['parameter']} (Level: {param['level_layer']}, "
            f"Forecast Valid: {param['forecast_valid']}, Number: {param['number']})"
        )

class Command(BaseCommand):
    help = 'Fetch and import GFS parameters from a text file'

    def handle(self, *args, **options):
        logger.info("Starting the GFS parameter import process from file.")

        file_path = "data/parameters.txt"  # Update the path to point to the data directory
        parameters = fetch_gfs_parameters_from_file(file_path)

        if parameters:
            delete_all_gfs_parameters()
            reset_gfs_parameter_id_sequence()
            import_gfs_parameters(parameters)
            logger.info("GFS parameter import process completed.")
        else:
            logger.error("No parameters were fetched.")
