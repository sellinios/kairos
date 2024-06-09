import os
import logging
import pygrib
from datetime import datetime, timezone, timedelta
from django.core.management.base import BaseCommand
from gfs_management.models import GFSParameter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_forecast_details_from_combined_filename(filename, cycle_hour, folder_name):
    try:
        base_name = os.path.basename(filename)
        parts = base_name.split('_')
        date_str = parts[1]
        forecast_hour_str = parts[2].split('.')[0]

        # Extract full UTC cycle information from folder name
        folder_parts = folder_name.split('_')
        utc_cycle_time_str = folder_parts[1]

        # Calculate the valid datetime and forecast hour
        cycle_datetime = datetime.strptime(f"{date_str}{utc_cycle_time_str}", "%Y%m%d%H").replace(tzinfo=timezone.utc)
        forecast_hour = int(forecast_hour_str)
        valid_datetime = cycle_datetime + timedelta(hours=forecast_hour)

        return valid_datetime, cycle_datetime, forecast_hour, utc_cycle_time_str
    except Exception as e:
        logger.error(f"Error extracting details from filename {filename}: {e}")
        return None, None, None, None

def list_available_parameters(file_path):
    parameters = set()
    try:
        with pygrib.open(file_path) as gribs:
            for grib in gribs:
                param_key = (grib.parameterCategory, grib.level, grib.shortName, grib.name)
                parameters.add(param_key)
    except Exception as e:
        logger.error(f"Error listing parameters in GRIB file {file_path}: {e}")
    return parameters

def standardize_param_key(param):
    """Standardize the parameter key for consistent comparison."""
    return (param[0], param[1], param[2].lower(), param[3].lower())

def filter_grib_messages(file_path, relevant_parameters, new_file_path, valid_datetime, cycle_datetime, forecast_hour, utc_cycle_time_str):
    try:
        with pygrib.open(file_path) as gribs, open(new_file_path, 'wb') as new_grib_file:
            for grib in gribs:
                param_key = standardize_param_key((grib.parameterCategory, grib.level, grib.shortName, grib.name))
                if param_key in relevant_parameters:
                    new_grib_file.write(grib.tostring())
                    logger.info(f"Saved message: Parameter: {grib.shortName}, Level: {grib.level}, Type of Level: {grib.name}")
                else:
                    logger.debug(f"Skipping message: Parameter: {grib.shortName}, Level: {grib.level}, Type of Level: {grib.name}")
    except Exception as e:
        logger.error(f"Unexpected error while filtering GRIB file {file_path}: {e}")

class Command(BaseCommand):
    """
    Filter and save GRIB data based on enabled parameters in the database.
    """

    help = 'Filter and save GRIB data based on enabled parameters in the database'

    def handle(self, *args, **options):
        logger.info("Starting the GRIB data filtering process.")

        base_directory = "data"
        filtered_directory = os.path.join(base_directory, "filtered_data")
        os.makedirs(filtered_directory, exist_ok=True)

        subdirectories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d)) and d.startswith("2024")]
        if not subdirectories:
            logger.error("No valid data directories found in the base directory.")
            return

        try:
            # Log enabled parameters with details
            relevant_parameters = {
                standardize_param_key((param.number, param.level_layer, param.parameter, param.description)): param
                for param in GFSParameter.objects.filter(enabled=True)
            }
            if not relevant_parameters:
                logger.warning("No enabled parameters found.")
                return

            logger.info(f"Enabled parameters: {list(relevant_parameters.keys())}")

            for subdirectory in subdirectories:
                subdirectory_path = os.path.join(base_directory, subdirectory)
                cycle_hour = subdirectory.split('_')[1]

                filtered_subdirectory = os.path.join(filtered_directory, subdirectory)
                os.makedirs(filtered_subdirectory, exist_ok=True)

                for filename in os.listdir(subdirectory_path):
                    if filename.endswith('.grib2'):
                        file_path = os.path.join(subdirectory_path, filename)
                        valid_datetime, cycle_datetime, forecast_hour, utc_cycle_time_str = extract_forecast_details_from_combined_filename(filename, cycle_hour, subdirectory)
                        if valid_datetime is None:
                            logger.error(f"Skipping file due to error in extracting details: {file_path}")
                            continue

                        # Updated file naming convention
                        new_file_name = f"filtered_{valid_datetime.strftime('%Y%m%d_%H')}_{forecast_hour:03d}.grib2"
                        new_file_path = os.path.join(filtered_subdirectory, new_file_name)

                        # Check available parameters in the GRIB file
                        available_parameters = list_available_parameters(file_path)
                        logger.info(f"Available parameters in {file_path}: {available_parameters}")

                        # Standardize available parameters
                        standardized_available_parameters = {standardize_param_key(param) for param in available_parameters}

                        # Log details of matching attempts
                        relevant_and_available_parameters = set()
                        for param in relevant_parameters:
                            if param in standardized_available_parameters:
                                relevant_and_available_parameters.add(param)
                            else:
                                logger.debug(f"Parameter {param} not found in available parameters.")

                        if relevant_and_available_parameters:
                            logger.info(f"Filtering data from {file_path} to {new_file_path}")
                            filter_grib_messages(file_path, relevant_and_available_parameters, new_file_path, valid_datetime, cycle_datetime, forecast_hour, utc_cycle_time_str)
                        else:
                            # Additional check for '2 metre temperature'
                            specific_param = standardize_param_key((0, 2, '2t', '2 metre temperature'))
                            if specific_param in standardized_available_parameters:
                                logger.info(f"Specifically found '2 metre temperature' in {file_path}. Adding to filter.")
                                relevant_and_available_parameters.add(specific_param)
                                filter_grib_messages(file_path, relevant_and_available_parameters, new_file_path, valid_datetime, cycle_datetime, forecast_hour, utc_cycle_time_str)
                            else:
                                logger.warning(f"No relevant parameters found in {file_path}. Skipping file.")

            logger.info("GRIB data filtering process completed.")

        except Exception as e:
            logger.error(f"Error during the filtering process: {e}")

