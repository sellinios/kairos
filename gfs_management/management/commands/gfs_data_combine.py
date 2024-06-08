import os
import logging
import pygrib
import numpy as np
import csv
from datetime import datetime, timezone
from shapely.geometry import Point
from django.core.management.base import BaseCommand
from weather.models import GFSForecast
from concurrent.futures import ThreadPoolExecutor
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_forecast_details_from_filename(filename):
    try:
        parts = filename.split('_')
        date_str = parts[1]  # Extracting '20240608'
        cycle_hour_str = parts[2]  # Extracting '06'
        forecast_hour_str = parts[3].split('.')[0]  # Extracting '000'

        # Create utc_cycle_time as datetime object
        utc_cycle_time = datetime.strptime(f"{date_str} {cycle_hour_str}", "%Y%m%d %H").replace(tzinfo=timezone.utc)

        # Convert forecast_hour_str to integer
        forecast_hour = int(forecast_hour_str)

        return utc_cycle_time, forecast_hour, date_str
    except Exception as e:
        logger.error("Error extracting details from filename %s: %s", filename, e)
        return None, None, None

def bulk_import_forecast_data(forecast_data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['id', 'latitude', 'longitude', 'forecast_data', 'date', 'hour', 'utc_cycle_time', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in forecast_data:
            if data['forecast_data']:
                writer.writerow(data)

    logger.info(f"Saved combined forecast data to {output_file}")

def process_grib_message(grib, utc_cycle_time, forecast_hour, date_str, chunk_size, current_id):
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
            'date': date_str,
            'hour': forecast_hour,
            'utc_cycle_time': utc_cycle_time.isoformat(),
            'location': Point(lon, lat).wkt
        })
        current_id += 1

        if len(forecast_data) >= chunk_size:
            break

    return forecast_data, current_id

def parse_and_import_gfs_data(file_path, chunk_size=10000):
    logger.info("Starting to parse GFS data from %s.", file_path)

    utc_cycle_time, forecast_hour, date_str = extract_forecast_details_from_filename(os.path.basename(file_path))
    if utc_cycle_time is None or forecast_hour is None or date_str is None:
        logger.error("Could not extract datetime details from filename: %s", file_path)
        return []

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
                logger.info("UTC cycle time is %s (UTC)", utc_cycle_time.isoformat())

                futures.append(executor.submit(process_grib_message, grib, utc_cycle_time, forecast_hour, date_str, chunk_size, current_id))

            for future in futures:
                result, new_id = future.result()
                forecast_data.extend(result)
                current_id = new_id

        return forecast_data

    except Exception as e:
        logger.error("Error processing GRIB file %s: %s", file_path, e)
        return []

def combine_forecast_data(data_dir):
    pattern = re.compile(r'^\d{8}_\d{2}$')  # Pattern to match directories like '20240608_06'
    combined_data = []

    for root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            if pattern.match(dir_name):
                dir_path = os.path.join(root, dir_name)
                logger.info(f"Processing directory: {dir_path}")
                for file_name in os.listdir(dir_path):
                    if file_name.endswith('.grib2'):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.exists(file_path):
                            try:
                                logger.info(f"Processing file: {file_path}")
                                data = parse_and_import_gfs_data(file_path)
                                combined_data.extend(data)
                            except Exception as e:
                                logger.error("Error processing file %s: %s", file_path, e)

    if combined_data:
        output_file = os.path.join(data_dir, 'combined_forecast_data.csv')
        bulk_import_forecast_data(combined_data, output_file)

class Command(BaseCommand):
    help = 'Combine and import GFS data into the database'

    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, default='data', help='Path to the directory containing GRIB2 files')

    def handle(self, *args, **options):
        logger.info("Starting the GFS data import process.")

        data_dir = options['dir']

        combine_forecast_data(data_dir)

        logger.info("GFS data import process completed.")
        logger.info("All files processed.")
