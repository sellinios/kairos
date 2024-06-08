import os
import logging
import pygrib
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from gfs_management.models import GFSParameter
from weather.models import GFSForecast
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_forecast_details_from_combined_filename(filename):
    try:
        base_name = os.path.basename(filename)
        parts = base_name.split('_')
        date_str = parts[1]
        hour_str = parts[2].split('.')[0]

        valid_datetime = datetime.strptime(f"{date_str}{hour_str}", "%Y%m%d%H").replace(tzinfo=timezone.utc)
        utc_cycle_time = valid_datetime
        forecast_hour = int(hour_str)

        return valid_datetime, utc_cycle_time, forecast_hour
    except Exception as e:
        logger.error(f"Error extracting details from filename {filename}: {e}")
        return None, None, None


def parse_and_import_gfs_data(file_path):
    logger.info("Starting to parse GFS data from %s.", file_path)

    valid_datetime, utc_cycle_time, forecast_hour = extract_forecast_details_from_combined_filename(
        os.path.basename(file_path))
    if valid_datetime is None or utc_cycle_time is None or forecast_hour is None:
        logger.error("Could not extract datetime details from filename: %s", file_path)
        return

    relevant_parameters = {param.number: param for param in GFSParameter.objects.all()}
    forecast_data = []

    try:
        gribs = pygrib.open(file_path)
        total_messages = gribs.messages
        logger.info("Total number of messages in the GRIB file: %d", total_messages)

        for i, grib in enumerate(gribs, start=1):
            param_number = grib.parameterCategory * 1000 + grib.parameterNumber
            if param_number in relevant_parameters:
                param = relevant_parameters[param_number]
                data = grib.values
                lats, lons = grib.latlons()

                if i % 10 == 0:  # Log progress every 10 messages
                    logger.info(
                        "Processing message %d of %d. Parameter: %s, Level: %d, Type of Level: %s",
                        i, total_messages, param.parameter, grib.level, grib.typeOfLevel
                    )
                    logger.info("Valid datetime is %s (UTC)", valid_datetime.isoformat())

                for lat, lon, value in zip(lats.flatten(), lons.flatten(), data.flatten()):
                    if isinstance(value, np.ma.core.MaskedConstant):
                        value = None

                    forecast_data.append({
                        'latitude': lat,
                        'longitude': lon,
                        'utc_cycle_time': utc_cycle_time,
                        'date': valid_datetime.date(),
                        'hour': valid_datetime.hour,
                        'param_name': param.parameter.lower().replace(' ', '_'),
                        'value': value
                    })

    except Exception as e:
        logger.error("Error processing GRIB file %s: %s", file_path, e)
        return

    forecast_data.sort(key=lambda x: (x['latitude'], x['longitude'], x['utc_cycle_time']))

    for data in forecast_data:
        if data['value'] is not None:
            forecast, created = GFSForecast.objects.get_or_create(
                latitude=data['latitude'],
                longitude=data['longitude'],
                utc_cycle_time=data['utc_cycle_time'],
                date=data['date'],
                hour=data['hour'],
                defaults={'forecast_data': {}}
            )

            forecast.forecast_data[data['param_name']] = data['value']
            forecast.save()
            logger.info(
                "Saved GFS forecast for coordinates (%.4f, %.4f) at %s (UTC) with parameter %s",
                data['latitude'], data['longitude'], data['utc_cycle_time'], data['param_name']
            )

    logger.info("Finished parsing GFS data from %s.", file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted GRIB file: %s", file_path)


class Command(BaseCommand):
    """
    Import GFS data into the database.
    """

    help = 'Import GFS data into the database'

    def handle(self, *args, **options):
        logger.info("Starting the GFS data import process.")

        combined_directory = "data/combined_data"
        if not os.path.exists(combined_directory):
            logger.error("Combined directory does not exist.")
            return

        for filename in os.listdir(combined_directory):
            if filename.endswith('.grib2'):
                file_path = os.path.join(combined_directory, filename)
                parse_and_import_gfs_data(file_path)

        logger.info("GFS data import process completed.")
