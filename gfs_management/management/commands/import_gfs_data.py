import logging
import os
import requests  # Import the requests module
from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand
from geography.models import Country
from gfs_management.models import GFSConfig, GFSParameter
from weather.utils import download_gfs_data_sequence, parse_and_import_gfs_data, extract_grib_parameters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import GFS data into the database'

    def handle(self, *args, **kwargs):
        logger.info("Starting the GFS data import process.")

        # Fetch all countries enabled for fetching forecasts
        countries = Country.objects.filter(fetch_forecasts=True)
        if not countries.exists():
            self.stdout.write(self.style.ERROR("No countries are enabled for fetching forecasts."))
            return

        now = datetime.utcnow()
        base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
        date = now.strftime("%Y%m%d")
        latest_hour = '06'  # Example value, adjust as needed
        save_directory = "data/gfs_files"

        for country in countries:
            logger.info(f"Processing country: {country.name}")

            # Find the GFSConfig for the country
            gfs_config = GFSConfig.objects.filter(countries=country).first()
            if not gfs_config:
                logger.error(f"No GFS configuration found for {country.name}.")
                continue

            # Get forecast hours from the configuration
            forecast_hours = gfs_config.get_forecast_hours()
            if not forecast_hours:
                logger.error("No forecast hours specified in GFS configuration.")
                continue

            logger.info(f"Forecast hours: {forecast_hours}")
            logger.info(f"Downloading GFS data for date: {date}, hour: {latest_hour}, forecast hours: {forecast_hours}")

            # Download GFS data for each hour and forecast hour combination
            download_gfs_data_sequence(base_url, date, [latest_hour], forecast_hours, save_directory)
            logger.info("GFS data download completed.")

            logger.info("Starting to extract GRIB parameters.")
            extracted_parameters = extract_grib_parameters(save_directory)
            logger.info(f"Extracted parameters: {extracted_parameters}")

            # Log the extracted parameters
            for param in extracted_parameters:
                logger.info(
                    f"Extracted parameter: {param['name']}, Description: {param['description']}, "
                    f"Level: {param['level']}, Type of Level: {param['type_of_level']}"
                )

            # Log the manually added GFS parameters
            manually_added_parameters = GFSParameter.objects.filter(
                name__in=["Convective precipitation", "Precipitation rate", "Minimum temperature", "Maximum temperature"]
            )
            for param in manually_added_parameters:
                logger.info(
                    f"Manually added parameter: {param.name}, Description: {param.description}, "
                    f"Level: {param.level}, Type of Level: {param.type_of_level}"
                )

            relevant_parameters = {(param.name, param.level, param.type_of_level): param.description for param in
                                   GFSParameter.objects.all()}

            logger.info("Starting to parse and import GFS data.")
            parse_and_import_gfs_data(save_directory, relevant_parameters, country, now)
            logger.info(f"GFS data import process completed for country: {country.name}")

            # Clean up GFS data files
            logger.info("Cleaning up GFS data files.")
            for filename in os.listdir(save_directory):
                file_path = os.path.join(save_directory, filename)
                if os.path.isfile(file_path) and filename.endswith(".grib2"):
                    os.remove(file_path)
                    logger.info(f"Deleted file: {file_path}")

        logger.info("All countries processed.")

import os
import logging
import numpy as np
from datetime import timezone, timedelta
from shapely.geometry import Point, shape
import geojson
import pygrib
from gfs_management.models import GFSParameter
from weather.models.model_gfs_forecast import GFSForecast

logger = logging.getLogger(__name__)

def download_gfs_data_sequence(base_url, date, hours, forecast_hours, save_directory):
    os.makedirs(save_directory, exist_ok=True)

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
                else:
                    logger.warning(f"Failed to download GFS data from {url}")

def extract_grib_parameters(directory):
    parameters = []
    logger.info("Starting to extract parameters from GRIB files.")
    for filename in os.listdir(directory):
        if filename.endswith(".grib2"):
            file_path = os.path.join(directory, filename)
            logger.info(f"Processing file: {file_path}")
            try:
                gribs = pygrib.open(file_path)
                for grib in gribs:
                    parameter = {
                        'name': grib.parameterName,
                        'description': grib.parameterUnits,
                        'level': grib.level,
                        'type_of_level': grib.typeOfLevel
                    }
                    logger.info(
                        f"Found parameter: {parameter['name']}, Description: {parameter['description']}, Level: {parameter['level']}, Type of Level: {parameter['type_of_level']}")
                    if parameter not in parameters:
                        parameters.append(parameter)
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
            break  # Stop after processing the first file
    logger.info(f"Extracted parameters: {parameters}")
    return parameters

def parse_and_import_gfs_data(directory, relevant_parameters, country, base_time):
    logger.info("Starting to parse GFS data.")

    try:
        # Convert the country geometry to GeoJSON and then to a Shapely shape
        country_geojson = geojson.loads(country.geom.geojson)
        country_shape = shape(country_geojson)
    except Exception as e:
        logger.error(f"Error converting country geometry: {e}")
        return

    for filename in os.listdir(directory):
        if filename.endswith(".grib2"):
            file_path = os.path.join(directory, filename)
            gribs = pygrib.open(file_path)
            total_messages = gribs.messages
            logger.info(f"Total number of messages in the GRIB file: {total_messages}")

            forecast_data = {}
            forecast_hour = int(filename.split("_")[-1].split(".")[0])  # Extract forecast hour from filename

            for i, grib in enumerate(gribs, start=1):
                param_key = (grib.parameterName, grib.level, grib.typeOfLevel)
                if param_key in relevant_parameters:
                    logger.info(
                        f"Processing message {i} of {total_messages}. Parameter: {grib.parameterName}, Level: {grib.level}, Type of Level: {grib.typeOfLevel}")

                    data = grib.values
                    lats, lons = grib.latlons()
                    valid_date = (base_time + timedelta(hours=forecast_hour)).replace(minute=0, second=0, microsecond=0)
                    valid_date = valid_date.replace(tzinfo=timezone.utc)

                    for lat, lon, value in zip(lats.flatten(), lons.flatten(), data.flatten()):
                        if isinstance(value, np.ma.core.MaskedConstant):
                            value = None

                        point = Point(lon, lat)
                        if not country_shape.contains(point):
                            continue

                        key = (lat, lon)
                        if key not in forecast_data:
                            forecast_data[key] = {
                                'latitude': lat,
                                'longitude': lon,
                                'timestamp': valid_date,
                                'forecast_hour': forecast_hour,  # Include forecast hour in the data
                                'data': {}
                            }

                        param_name = f"{grib.parameterName.lower().replace(' ', '_')}_level_{grib.level}_{grib.typeOfLevel}"
                        forecast_data[key]['data'][param_name] = value

            for key, data in forecast_data.items():
                forecast = GFSForecast(
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    forecast_data=data['data'],
                    timestamp=data['timestamp']
                )
                forecast.save()
                logger.info(
                    f"Saved GFS forecast for coordinates ({data['latitude']}, {data['longitude']}) at {data['timestamp']} with forecast hour {data['forecast_hour']}")

    logger.info("Finished parsing GFS data.")
