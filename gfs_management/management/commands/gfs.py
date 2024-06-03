from datetime import datetime
import logging
import os
from datetime import timedelta, timezone
import geojson
import numpy as np
import pygrib
import requests
from django.core.management.base import BaseCommand
from shapely.geometry import Point, shape
from geography.models import GeographicCountry
from gfs_management.models import GFSConfig, GFSParameter
from weather.models import GFSForecast
from weather.utils import extract_forecast_details_from_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_gfs_data_sequence(base_url, date, hours, forecast_hours, save_directory):
    os.makedirs(save_directory, exist_ok=True)
    grib_files = []

    for hour in hours:
        for forecast_hour in forecast_hours:
            file_name = f"gfs.t{hour}z.pgrb2.0p25.f{forecast_hour:03}"
            url = f"{base_url}/gfs.{date}/{hour}/atmos/{file_name}"
            save_path = os.path.join(save_directory, f"gfs_{date}_{hour}_{forecast_hour:03}.grib2")
            if not os.path.exists(save_path):
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    with open(save_path, 'wb') as file:
                        file.write(response.content)
                    logger.info("Downloaded GFS data to %s", save_path)
                    grib_files.append(save_path)
                else:
                    logger.warning("Failed to download GFS data from %s", url)
                    return False
            else:
                logger.info("File already exists: %s", save_path)
                grib_files.append(save_path)
    return grib_files

def parse_and_import_gfs_data(file_path, relevant_parameters, country):
    logger.info("Starting to parse GFS data from %s.", file_path)

    valid_datetime, utc_cycle_time, forecast_hour = extract_forecast_details_from_filename(os.path.basename(file_path))
    if valid_datetime is None or utc_cycle_time is None or forecast_hour is None:
        logger.error("Could not extract datetime details from filename: %s", file_path)
        return

    try:
        country_geojson = geojson.loads(country.geom.geojson)
        country_shape = shape(country_geojson)
    except Exception as e:
        logger.error("Error converting country geometry: %s", e)
        return

    forecast_data = []

    try:
        gribs = pygrib.open(file_path)
        total_messages = gribs.messages
        logger.info("Total number of messages in the GRIB file: %d", total_messages)

        for i, grib in enumerate(gribs, start=1):
            param_key = (grib.parameterName, grib.level, grib.typeOfLevel)
            if param_key in relevant_parameters:
                data = grib.values
                lats, lons = grib.latlons()

                logger.info(
                    "Processing message %d of %d. Parameter: %s, Level: %d, Type of Level: %s",
                    i, total_messages, grib.parameterName, grib.level, grib.typeOfLevel
                )
                logger.info("Valid datetime is %s (UTC)", valid_datetime.isoformat())

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
                        'utc_cycle_time': utc_cycle_time,
                        'date': valid_datetime.date(),
                        'hour': valid_datetime.hour,
                        'param_name': param_name,
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

    def add_arguments(self, parser):
        parser.add_argument('--base_url', type=str, default="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod")
        parser.add_argument('--date', type=str, default=None)
        parser.add_argument('--hours_to_try', nargs='+', type=str, default=['18', '12', '06', '00'])

    def handle(self, *args, **options):
        logger.info("Starting the GFS data import process.")

        base_url = options['base_url']
        if options['date']:
            date = options['date']
        else:
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
            date = now.strftime("%Y%m%d")

        hours_to_try = options['hours_to_try']

        def try_download(date, hours, forecast_hours):
            save_directory = "data/gfs_files"
            for hour in hours:
                grib_files = download_gfs_data_sequence(base_url, date, [hour], forecast_hours, save_directory)
                if grib_files:
                    return grib_files
            return None

        # Fetch the forecast hours from the GFSConfig model
        countries = GeographicCountry.objects.filter(fetch_forecasts=True)
        if not countries.exists():
            self.stdout.write(self.style.ERROR("No countries are enabled for fetching forecasts."))
            return

        for country in countries:
            try:
                logger.info("Processing country: %s", country.name)

                gfs_config = GFSConfig.objects.filter(countries=country).first()
                if not gfs_config:
                    logger.error("No GFS configuration found for %s.", country.name)
                    continue

                forecast_hours = gfs_config.get_forecast_hours()
                if not forecast_hours:
                    logger.error("No forecast hours specified in GFS configuration.")
                    continue

                parameters = gfs_config.parameters.all()
                if not parameters:
                    logger.error("No parameters specified in GFS configuration for %s.", country.name)
                    continue

                relevant_parameters = {(param.name, param.level, param.type_of_level): param.description for param in parameters}

                logger.info("Forecast hours: %s", forecast_hours)
                logger.info("Downloading GFS data for date: %s, hours: %s", date, hours_to_try)

                grib_files = try_download(date, hours_to_try, forecast_hours)
                if not grib_files:
                    logger.warning("Download failed, trying previous cycle.")
                    now -= timedelta(days=1)
                    date = now.strftime("%Y%m%d")
                    grib_files = try_download(date, hours_to_try, forecast_hours)
                    if not grib_files:
                        logger.error("Download failed again, aborting.")
                        return

                for grib_file in grib_files:
                    parse_and_import_gfs_data(grib_file, relevant_parameters, country)

                logger.info("GFS data import process completed for country: %s", country.name)

                logger.info("Cleaning up GFS data files.")
                save_directory = "data/gfs_files"
                for filename in os.listdir(save_directory):
                    file_path = os.path.join(save_directory, filename)
                    if os.path.isfile(file_path) and filename.endswith(".grib2"):
                        os.remove(file_path)
                        logger.info("Deleted file: %s", file_path)

            except Exception as e:
                logger.error("Error processing country %s: %s", country.name, e)

        logger.info("All countries processed.")