import os
import logging
import pygrib
import numpy as np
from datetime import datetime, timezone
from shapely.geometry import Point
from django.core.management.base import BaseCommand
from weather.models import GFSForecast
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_forecast_details_from_filename(filename):
    try:
        parts = filename.split('_')
        date_str = parts[2]
        hour_str = parts[3].split('.')[0]
        valid_datetime = datetime.strptime(f"{date_str} {hour_str}", "%Y%m%d %H").replace(tzinfo=timezone.utc)
        return valid_datetime, int(hour_str)
    except Exception as e:
        logger.error("Error extracting details from filename %s: %s", filename, e)
        return None, None

def bulk_import_forecast_data(forecast_data):
    for data in forecast_data:
        if data['forecast_data']:
            forecast, created = GFSForecast.objects.get_or_create(
                latitude=data['latitude'],
                longitude=data['longitude'],
                utc_cycle_time=datetime.fromisoformat(data['utc_cycle_time']),
                date=data['date'],
                hour=data['hour'],
                defaults={'forecast_data': {}}
            )

            forecast.forecast_data.update(data['forecast_data'])
            forecast.save()
            logger.info(
                "Saved GFS forecast for coordinates (%.4f, %.4f) at %s (UTC)",
                data['latitude'], data['longitude'], data['utc_cycle_time']
            )

def process_grib_message(grib, valid_datetime, chunk_size, current_id):
    forecast_data = []
    data = grib.values
    lats, lons = grib.latlons()

    param_name = f"{grib.parameterName.lower().replace(' ', '_')}_level_{grib.level}_{grib.typeOfLevel}"

    for lat, lon, value in zip(lats.flatten(), lons.flatten(), data.flatten()):
        if isinstance(value, np.ma.core.MaskedConstant):
            value = None

        forecast_data.append({
            'id': current_id,
            'latitude': lat,
            'longitude': lon,
            'forecast_data': {param_name: value},
            'date': valid_datetime.date().isoformat(),
            'hour': valid_datetime.hour,
            'utc_cycle_time': valid_datetime.isoformat(),
            'location': Point(lon, lat).wkt
        })
        current_id += 1

        if len(forecast_data) >= chunk_size:
            bulk_import_forecast_data(forecast_data)
            forecast_data = []

    return forecast_data, current_id

def parse_and_import_gfs_data(file_path, chunk_size=10000):
    logger.info("Starting to parse GFS data from %s.", file_path)

    valid_datetime, utc_cycle_time = extract_forecast_details_from_filename(os.path.basename(file_path))
    if valid_datetime is None or utc_cycle_time is None:
        logger.error("Could not extract datetime details from filename: %s", file_path)
        return

    try:
        gribs = pygrib.open(file_path)
        total_messages = gribs.messages
        logger.info("Total number of messages in the GRIB file: %d", total_messages)

        forecast_data = []
        current_id = 1  # Reset ID for each file import

        with ThreadPoolExecutor() as executor:
            futures = []
            for i, grib in enumerate(gribs, start=1):
                logger.info(
                    "Processing message %d of %d. Parameter: %s, Level: %d, Type of Level: %s",
                    i, total_messages, grib.parameterName, grib.level, grib.typeOfLevel
                )
                logger.info("Valid datetime is %s (UTC)", valid_datetime.isoformat())

                futures.append(executor.submit(process_grib_message, grib, valid_datetime, chunk_size, current_id))

            for future in futures:
                result, new_id = future.result()
                forecast_data.extend(result)
                current_id = new_id

        if forecast_data:
            bulk_import_forecast_data(forecast_data)

    except Exception as e:
        logger.error("Error processing GRIB file %s: %s", file_path, e)
        return

    logger.info("Finished parsing GFS data from %s.", file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted GRIB file: %s", file_path)

class Command(BaseCommand):
    help = 'Import GFS data into the database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to the filtered GRIB2 file')

    def handle(self, *args, **options):
        logger.info("Starting the GFS data import process.")

        file_path = options['file'] or 'data/filtered_data/filtered_combined_20240608_06.grib2'  # Default path

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return

        try:
            logger.info("Processing file: %s", file_path)
            parse_and_import_gfs_data(file_path)
            logger.info("GFS data import process completed.")
        except Exception as e:
            logger.error("Error processing file %s: %s", file_path, e)

        logger.info("All files processed.")
