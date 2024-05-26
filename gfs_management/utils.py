# weather/utils.py

import os
import logging
from some_grib_library import open_grib_file
from gfs_management.models import GFSParameter

logger = logging.getLogger(__name__)


def download_gfs_data_sequence(base_url, date, hours, forecast_hours, save_directory):
    # Implementation for downloading GFS data files
    pass


def parse_and_import_gfs_data(directory, bounding_box, existing_parameters):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file.endswith('.grib2'):
            logger.info(f"Processing file: {file_path}")
            with open_grib_file(file_path) as grib:
                for message in grib:
                    param_name = message['parameterName']
                    param_desc = message['parameterDescription']

                    if param_name not in existing_parameters:
                        GFSParameter.objects.get_or_create(
                            name=param_name,
                            defaults={'description': param_desc}
                        )
                        existing_parameters[param_name] = param_desc

    logger.info("Parameters have been stored in the database.")
