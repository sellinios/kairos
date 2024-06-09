import os
import logging
import pygrib
import numpy as np
from datetime import datetime, timezone
from django.contrib.gis.geos import Point as GEOSPoint
from django.core.management.base import BaseCommand
from weather.models import GFSForecast
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_forecast_details_from_filename(filename):
    try:
        base_name = os.path.basename(filename)
        parts = base_name.split('_')

        if parts[0] == 'filtered':
            # Format: filtered_YYYYMMDD_HH_XXX.grib2
            date_str = parts[1]
            hour_str = parts[2]
            forecast_hour_str = parts[3].split('.')[0]

            # Construct datetime objects
            valid_datetime = datetime.strptime(f"{date_str}{hour_str}", "%Y%m%d%H").replace(tzinfo=timezone.utc)
            utc_cycle_time = hour_str  # Cycle time as string

        else:
            # Format: gfs_YYYYMMDD_CC_FFF_YYYYMMDDHH.grib2
            date_str = parts[2]
            cycle_str = parts[3]
            forecast_hour_str = parts[4]
            valid_datetime_str = parts[5].split('.')[0]

            if cycle_str not in {'00', '06', '12', '18'}:
                raise ValueError(f"Invalid cycle time: {cycle_str}")

            valid_datetime = datetime.strptime(valid_datetime_str, "%Y%m%d%H").replace(tzinfo=timezone.utc)
            utc_cycle_time = cycle_str

        return valid_datetime, utc_cycle_time
    except Exception as e:
        logger.error(f"Error extracting details from filename {filename}: {e}")
        return None, None

def bulk_import_forecast_data(forecast_data):
    try:
        GFSForecast.objects.bulk_create(
            [GFSForecast(
                latitude=data['latitude'],
                longitude=data['longitude'],
                date=data['date'],
                hour=data['hour'],
                utc_cycle_time=data['utc_cycle_time'],
                forecast_data=data['forecast_data'],
                location=GEOSPoint(data['longitude'], data['latitude'])  # Use GEOSPoint instead of shapely Point
            ) for data in forecast_data],
            batch_size=1000  # Adjust batch size as needed
        )
        logger.info("Bulk inserted %d records", len(forecast_data))
    except Exception as e:
        logger.error(f"Error during bulk insert: {e}")

def process_grib_message(grib, valid_datetime, utc_cycle_time, chunk_size):
    forecast_data = []
    data = grib.values
    lats, lons = grib.latlons()

    param_name = f"{grib.parameterName.lower().replace(' ', '_')}_level_{grib.level}_{grib.typeOfLevel}"

    for lat, lon, value in zip(lats.flatten(), lons.flatten(), data.flatten()):
        if isinstance(value, np.ma.core.MaskedConstant):
            value = None

        forecast_data.append({
            'latitude': lat,
            'longitude': lon,
            'forecast_data': {param_name: value},
            'date': str(valid_datetime.date()),  # Ensure it's a string
            'hour': str(valid_datetime.hour),  # Ensure it's a string
            'utc_cycle_time': utc_cycle_time,  # Ensure this is a string
        })

        if len(forecast_data) >= chunk_size:
            bulk_import_forecast_data(forecast_data)
            forecast_data = []

    if forecast_data:
        bulk_import_forecast_data(forecast_data)

def parse_and_import_gfs_data(file_path, chunk_size=10000):
    logger.info("Starting to parse GFS data from %s.", file_path)

    valid_datetime, utc_cycle_time = extract_forecast_details_from_filename(file_path)
    if valid_datetime is None or utc_cycle_time is None:
        logger.error("Could not extract datetime details from filename: %s", file_path)
        return

    try:
        with pygrib.open(file_path) as gribs:
            total_messages = gribs.messages
            logger.info("Total number of messages in the GRIB file: %d", total_messages)

            with ThreadPoolExecutor() as executor:
                futures = []
                for i, grib in enumerate(gribs, start=1):
                    logger.info(
                        "Processing message %d of %d. Parameter: %s, Level: %d, Type of Level: %s",
                        i, total_messages, grib.parameterName, grib.level, grib.typeOfLevel
                    )
                    logger.info("Valid datetime is %s (UTC)", valid_datetime.isoformat())

                    futures.append(
                        executor.submit(process_grib_message, grib, valid_datetime, utc_cycle_time, chunk_size))

                for future in futures:
                    future.result()

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
