import os
import requests
import logging
import numpy as np
from datetime import timezone
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

def parse_and_import_gfs_data(directory, relevant_parameters, country):
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

            for i, grib in enumerate(gribs, start=1):
                param_key = (grib.parameterName, grib.level, grib.typeOfLevel)
                if param_key in relevant_parameters:
                    logger.info(
                        f"Processing message {i} of {total_messages}. Parameter: {grib.parameterName}, Level: {grib.level}, Type of Level: {grib.typeOfLevel}")

                    data = grib.values
                    lats, lons = grib.latlons()
                    valid_date = grib.validDate.replace(tzinfo=timezone.utc)

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
                    f"Saved GFS forecast for coordinates ({data['latitude']}, {data['longitude']}) at {data['timestamp']}")

    logger.info("Finished parsing GFS data.")
