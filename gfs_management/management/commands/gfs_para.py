import logging
import os
from datetime import datetime, timezone
import requests
import pygrib
from django.core.management.base import BaseCommand
from django.db import models  # Import the models module
from gfs_management.models import GFSParameter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_gfs_data(base_url, date, hour, forecast_hour, save_directory):
    os.makedirs(save_directory, exist_ok=True)
    file_name = f"gfs.t{hour}z.pgrb2.0p25.f{forecast_hour:03}"
    url = f"{base_url}/gfs.{date}/{hour}/atmos/{file_name}"
    save_path = os.path.join(save_directory, f"gfs_{date}_{hour}_{forecast_hour:03}.grib2")

    if not os.path.exists(save_path):
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            logger.info("Downloaded GFS data to %s", save_path)
            return save_path
        else:
            logger.warning("Failed to download GFS data from %s", url)
            return None
    else:
        logger.info("File already exists: %s", save_path)
        return save_path


def get_next_parameter_id():
    """Fetch the maximum parameter_id from the database and return the next incremental value."""
    max_id = GFSParameter.objects.aggregate(models.Max('parameter_id'))['parameter_id__max']
    return 1 if max_id is None else max_id + 1


def import_gfs_parameters(file_path):
    logger.info("Starting to parse GFS data from %s.", file_path)

    try:
        gribs = pygrib.open(file_path)
        total_messages = gribs.messages
        logger.info("Total number of messages in the GRIB file: %d", total_messages)

        for i, grib in enumerate(gribs, start=1):
            param_name = grib.parameterName
            level = grib.level
            type_of_level = grib.typeOfLevel

            # Get the next parameter ID
            parameter_id = get_next_parameter_id()

            # Save or update the parameter in the database
            parameter, created = GFSParameter.objects.update_or_create(
                name=param_name,
                level=level,
                type_of_level=type_of_level,
                defaults={'description': f'{param_name} at level {level} of type {type_of_level}',
                          'parameter_id': parameter_id}
            )

            logger.info(
                "Saved GFS parameter: %s (Level: %d, Type of Level: %s, ID: %d)",
                param_name, level, type_of_level, parameter_id
            )

    except Exception as e:
        logger.error("Error processing GRIB file %s: %s", file_path, e)
        return

    logger.info("Finished parsing GFS data from %s.", file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted GRIB file: %s", file_path)


class Command(BaseCommand):
    """
    Import GFS parameters into the database.
    """

    help = 'Download a GFS data file and import parameters into the database'

    def handle(self, *args, **options):
        logger.info("Starting the GFS data import process.")

        base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        date = now.strftime("%Y%m%d")
        hour = '00'
        forecast_hour = 1  # Change to 1 to download the 001 file
        save_directory = "data/gfs_files"

        try:
            logger.info("Downloading GFS data for date: %s, hour: %s", date, hour)

            grib_file = download_gfs_data(base_url, date, hour, forecast_hour, save_directory)
            if not grib_file:
                logger.error("Download failed, aborting.")
                return

            import_gfs_parameters(grib_file)

            logger.info("GFS data import process completed.")

        except Exception as e:
            logger.error("Error during the GFS data import process: %s", e)

        logger.info("Process completed.")
