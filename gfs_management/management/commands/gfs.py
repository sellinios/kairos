import os
import re
import requests
import logging
import pygrib
import numpy as np
from datetime import datetime, timedelta, timezone
from shapely.geometry import Point, shape
import geojson
from django.core.management.base import BaseCommand
from geography.models import Country
from gfs_management.models import GFSConfig, GFSParameter
from weather.models.model_gfs_forecast import GFSForecast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Utility functions
def get_latest_available_hour(base_url, date):
    available_hours = ['00', '06', '12', '18']
    for hour in reversed(available_hours):
        url = f"{base_url}/gfs.{date}/{hour}/"
        response = requests.head(url)
        if response.status_code == 200:
            return hour
    return None

def download_gfs_data_sequence(base_url, date, hours, forecast_hours, save_directory):
    os.makedirs(save_directory, exist_ok=True)
    grib_files = []

    for hour in hours:
        for forecast_hour in forecast_hours:
            file_name = f"gfs.t{hour}z.pgrb2.0p25.f{forecast_hour:03}"
            url = f"{base_url}/gfs.{date}/{hour}/atmos/{file_name}"
            save_path = os.path.join(save_directory, f"gfs_{date}_{hour}_{forecast_hour:03}.grib2")
            if not os.path.exists(save_path):
                response = requests.get(url)
                if response.status_code == 200:
                    with open(save_path, 'wb') as file:
                        file.write(response.content)
                    logger.info(f"Downloaded GFS data to {save_path}")
                    grib_files.append(save_path)
                else:
                    logger.warning(f"Failed to download GFS data from {url}")
            else:
                logger.info(f"File already exists: {save_path}")
                grib_files.append(save_path)
    return grib_files

def extract_forecast_hour_from_filename(filename):
    match = re.search(r'gfs_\d{8}_\d{2}_(\d{3})\.grib2', filename)
    if match:
        return int(match.group(1))
    return None

def parse_and_import_gfs_data(file_path, relevant_parameters, country, base_time):
    logger.info(f"Starting to parse GFS data from {file_path}.")

    forecast_hour = extract_forecast_hour_from_filename(os.path.basename(file_path))
    if forecast_hour is None:
        logger.error(f"Could not extract forecast hour from filename: {file_path}")
        return

    try:
        country_geojson = geojson.loads(country.geom.geojson)
        country_shape = shape(country_geojson)
    except Exception as e:
        logger.error(f"Error converting country geometry: {e}")
        return

    forecast_data = []

    try:
        gribs = pygrib.open(file_path)
        total_messages = gribs.messages
        logger.info(f"Total number of messages in the GRIB file: {total_messages}")

        valid_date = base_time + timedelta(hours=forecast_hour - 1)

        for i, grib in enumerate(gribs, start=1):
            param_key = (grib.parameterName, grib.level, grib.typeOfLevel)
            if param_key in relevant_parameters:
                data = grib.values
                lats, lons = grib.latlons()

                logger.info(f"Processing message {i} of {total_messages}. Parameter: {grib.parameterName}, Level: {grib.level}, Type of Level: {grib.typeOfLevel}")
                logger.info(f"Valid date for forecast hour {forecast_hour} is {valid_date.isoformat()} (UTC)")

                for lat, lon, value in zip(lats.flatten(), lons.flatten(), data.flatten()):
                    if isinstance(value, np.ma.core.MaskedConstant):
                        value = None

                    point = Point(lon, lat)
                    if not country_shape.contains(point):
                        continue

                    param_name = f"{grib.parameterName.lower().replace(' ', '_')}_level_{grib.level}_{grib.typeOfLevel}"
                    forecast_data.append({
                        'latitude': lat,
                        'longitude': lon,
                        'timestamp': valid_date,
                        'forecast_hour': forecast_hour,
                        'param_name': param_name,
                        'value': value
                    })
    except Exception as e:
        logger.error(f"Error processing GRIB file {file_path}: {e}")
        return

    forecast_data.sort(key=lambda x: (x['latitude'], x['longitude'], x['timestamp']))

    for data in forecast_data:
        if data['value'] is not None:
            forecast, created = GFSForecast.objects.get_or_create(
                latitude=data['latitude'],
                longitude=data['longitude'],
                timestamp=data['timestamp'],
                defaults={'forecast_data': {}}
            )

            forecast.forecast_data[data['param_name']] = data['value']
            forecast.save()
            logger.info(f"Saved GFS forecast for coordinates ({data['latitude']}, {data['longitude']}) at {data['timestamp']} (UTC) with forecast hour {data['forecast_hour']}")

    logger.info(f"Finished parsing GFS data from {file_path}.")

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"Deleted GRIB file: {file_path}")

class Command(BaseCommand):
    help = 'Import GFS data into the database'

    def handle(self, *args, **kwargs):
        logger.info("Starting the GFS data import process.")

        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
        date = now.strftime("%Y%m%d")

        latest_hour = get_latest_available_hour(base_url, date)
        if latest_hour is None:
            logger.error("No available GFS data found for the specified date.")
            return

        now = now.replace(hour=int(latest_hour), minute=0, second=0, microsecond=0)

        save_directory = "data/gfs_files"

        countries = Country.objects.filter(fetch_forecasts=True)
        if not countries.exists():
            self.stdout.write(self.style.ERROR("No countries are enabled for fetching forecasts."))
            return

        for country in countries:
            logger.info(f"Processing country: {country.name}")

            gfs_config = GFSConfig.objects.filter(countries=country).first()
            if not gfs_config:
                logger.error(f"No GFS configuration found for {country.name}.")
                continue

            forecast_hours = gfs_config.get_forecast_hours()
            if not forecast_hours:
                logger.error("No forecast hours specified in GFS configuration.")
                continue

            logger.info(f"Forecast hours: {forecast_hours}")
            logger.info(f"Downloading GFS data for date: {date}, hour: {latest_hour}, forecast hours: {forecast_hours}")

            grib_files = download_gfs_data_sequence(base_url, date, [latest_hour], forecast_hours, save_directory)

            relevant_parameters = {(param.name, param.level, param.type_of_level): param.description for param in GFSParameter.objects.all()}

            for grib_file in grib_files:
                parse_and_import_gfs_data(grib_file, relevant_parameters, country, now)

            logger.info(f"GFS data import process completed for country: {country.name}")

            logger.info("Cleaning up GFS data files.")
            for filename in os.listdir(save_directory):
                file_path = os.path.join(save_directory, filename)
                if os.path.isfile(file_path) and filename.endswith(".grib2"):
                    os.remove(file_path)
                    logger.info(f"Deleted file: {file_path}")

        logger.info("All countries processed.")