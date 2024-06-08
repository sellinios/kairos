import os
import logging
import pygrib
import json
import numpy as np
from datetime import datetime, timezone
from shapely.geometry import Point
from django.core.management.base import BaseCommand
from weather.models import GFSForecast
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_forecast_details_from_metadata(file_path):
    try:
        metadata_file = file_path.replace('.grib2', '_metadata.json')
        with open(metadata_file, 'r') as mf:
            metadata = json.load(mf)
            valid_datetime = datetime.fromisoformat(metadata["valid_datetime"])
            utc_cycle_time = metadata["utc_cycle_time"]
            forecast_hour = metadata["forecast_hour"]
            return valid_datetime, utc_cycle_time, forecast_hour
    except Exception as e:
        logger.error("Error extracting details from metadata file %s: %s", file_path, e)
        return None, None, None

def bulk_import_forecast_data(forecast_data):
    for data in forecast_data:
        if data['forecast_data']:
            forecast, created = GFSForecast.objects.get_or_create(
                latitude=data['latitude'],
                longitude=data['longitude'],
                date=data['date'],  # Ensure this is a string
                hour=data['hour'],  # Ensure this is a string
                utc_cycle_time=data['utc_cycle_time'],
                defaults={'forecast_data': {}}
            )

            forecast.forecast_data.update(data['forecast_data'])
            forecast.save()
            logger.info(
                "Saved GFS forecast for coordinates (%.4f, %.4f) at cycle %02d (UTC)",
                data['latitude'], data['longitude'], data['utc_cycle_time']
            )

def process_grib_message(grib, valid_datetime, utc_cycle_time, chunk_size, current_id):
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
            'date': str(valid_datetime.date()),  # Ensure it's a string
            'hour': str(valid_datetime.hour),  # Ensure it's a string
            'utc_cycle_time': utc_cycle_time,
            'location': Point(lon, lat).wkt
        })
        current_id += 1

        if len(forecast_data) >= chunk_size:
            bulk_import_forecast_data(forecast_data)
            forecast_data = []

    return forecast_data, current_id

def parse_and_import_gfs_data(file_path, chunk_size=10000):
    logger.info("Starting to parse GFS data from %s.", file_path)

    valid_datetime, utc_cycle_time, forecast_hour = extract_forecast_details_from_metadata(file_path)
    if valid_datetime is None or utc_cycle_time is None or forecast_hour is None:
        logger.error("Could not extract datetime details from metadata file: %s", file_path)
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

                futures.append(
                    executor.submit(process_grib_message, grib, valid_datetime, utc_cycle_time, chunk_size, current_id))

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

        file_path = options['file']
        if file_path:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return

            try:
                parse_and_import_gfs_data(file_path)
            except Exception as e:
                logger.error("An error occurred during the GFS data import process: %s", e)
        else:
            filtered_directory = 'data/filtered_data'
            if not os.path.exists(filtered_directory):
                logger.error(f"Filtered directory not found: {filtered_directory}")
                return

            for root, dirs, files in os.walk(filtered_directory):
                for file in files:
                    if file.endswith('.grib2'):
                        file_path = os.path.join(root, file)
                        try:
                            logger.info("Processing file: %s", file_path)
                            parse_and_import_gfs_data(file_path)
                        except Exception as e:
                            logger.error("Error processing file %s: %s", file_path, e)

            logger.info("GFS data import process completed for all files.")

        logger.info("All files processed.")
