import os
import logging
import pygrib
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_gfs_parameters(file_path, output_file):
    parameters = []
    try:
        with pygrib.open(file_path) as gribs:
            for grib in gribs:
                try:
                    param_number = grib['parameterNumber']
                    level_layer = grib['typeOfLevel']
                    parameter = grib['shortName']
                    forecast_valid = grib['level']
                    description = grib['name']
                    parameters.append({
                        "number": param_number,
                        "level_layer": level_layer,
                        "parameter": parameter,
                        "forecast_valid": forecast_valid,
                        "description": description
                    })
                except KeyError as e:
                    logger.error(f"KeyError while reading GRIB message: {e}")
    except Exception as e:
        logger.error(f"Error reading GRIB2 file: {e}")

    logger.info(f"Fetched and parsed {len(parameters)} GFS parameters from the file.")

    try:
        with open(output_file, 'w') as f:
            f.write("NUMBER\tLEVEL_LAYER\tPARAMETER\tFORECAST_VALID\tDESCRIPTION\n")
            for param in parameters:
                f.write(f"{param['number']}\t{param['level_layer']}\t{param['parameter']}\t{param['forecast_valid']}\t{param['description']}\n")
        logger.info(f"Parameters written to {output_file}")
    except Exception as e:
        logger.error(f"Error writing to file {output_file}: {e}")

class Command(BaseCommand):
    help = 'Extract and save GFS parameters to a text file'

    def handle(self, *args, **options):
        logger.info("Starting the GFS parameter extraction process from GRIB2 file.")

        input_file = "data/control.grib2"
        output_file = "data/parameters.txt"

        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return

        extract_gfs_parameters(input_file, output_file)
        logger.info("GFS parameter extraction process completed.")

