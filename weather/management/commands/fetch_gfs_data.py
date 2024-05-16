import os
import logging
import cfgrib
import pandas as pd
import requests

from django.core.management.base import BaseCommand
from django.utils import timezone
from weather.models import GFSForecast
from geography.models import Place

# Setup logging
logging.basicConfig(level=logging.INFO)


def load_grib_file(file_path, filters):
    """Loads data from a GRIB file with specified filters."""
    try:
        ds = cfgrib.open_dataset(
            file_path, filter_by_keys=filters, backend_kwargs={"indexpath": ""}
        )
        logging.info(f"Successfully loaded data with filter {filters} from file {file_path}")
        return ds
    except FileNotFoundError as e:
        logging.warning(
            f"Skipping file {file_path} with filter {filters}. File not found: {e}"
        )
        return None
    except Exception as e:
        logging.error(
            f"Failed to load data from file {file_path} with filter {filters}: {e}"
        )
        return None


class Command(BaseCommand):
    help = "Fetch and process GFS data"

    def handle(self, *args, **options):
        # GFS data configuration
        base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs"
        now = timezone.now()

        # Calculate the nearest available GFS cycle
        forecast_hours = [0, 6, 12, 18]
        forecast_hour = max([hour for hour in forecast_hours if hour <= now.hour])
        date_str = now.strftime("%Y%m%d")
        cycle = f"{forecast_hour:02d}"

        # Local storage for downloaded GRIB2 files
        grib2_dir = "./grib2_files"
        os.makedirs(grib2_dir, exist_ok=True)

        # Download the GRIB2 files if they don't exist
        for forecast_interval in range(0, 6, 1):
            file_name = f"gfs.t{cycle}z.pgrb2.0p25.f{forecast_interval:03d}"
            file_url = f"{base_url}.{date_str}/{cycle}/atmos/{file_name}"
            local_file_path = os.path.join(grib2_dir, file_name)

            if not os.path.exists(local_file_path):
                self.stdout.write(f"Downloading {file_name}...")
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(local_file_path, "wb") as f:
                        f.write(response.content)
                else:
                    self.stderr.write(f"Failed to download {file_url}")
            else:
                self.stdout.write(f"{file_name} already downloaded.")

        # Filters to extract specific data types from the GRIB2 files
        filters_list = [
            {"typeOfLevel": "meanSea"},
            {"typeOfLevel": "surface", "stepType": "instant"},
            {"typeOfLevel": "heightAboveGround", "level": 2},
            {"typeOfLevel": "isobaricInhPa", "level": 500},
        ]

        # Process each downloaded file with different filters
        for file_path in os.listdir(grib2_dir):
            if file_path.endswith(".grib2"):
                for filters in filters_list:
                    ds = load_grib_file(os.path.join(grib2_dir, file_path), filters)
                    if ds:
                        self.process_dataset(ds, filters)

    def process_dataset(self, ds, filters):
        """Processes a dataset, extracting and saving weather data."""
        # Check for 'time' coordinate
        if "time" not in ds.coords:
            logging.error(f"No 'time' coordinate with filters {filters}")
            return

        # Convert and standardize time values
        times = pd.to_datetime(ds.coords["time"].values)
        if not isinstance(times, pd.DatetimeIndex):
            times = pd.DatetimeIndex([times])  # Convert to list if single Timestamp

        times = times.tz_localize("UTC")  # Set timezone to UTC

        # Iterate over each time point and extract data
        for time in times:
            data_points = self.extract_data(ds, time)
            if data_points:
                self.save_data(data_points, time)

    def extract_data(self, ds, time):
        data_point = {}
        if 't2m' in ds.variables:
            data_point['temperature'] = ds['t2m'].sel(time=time).item()
        if 'prate' in ds.variables:
            data_point['precipitation'] = ds['prate'].sel(time=time).item()
        if 'wind_speed' in ds.variables:
            data_point['wind_speed'] = ds['wind_speed'].sel(time=time).item()
        return data_point

    def save_data(self, data_points, time):
        # Insert database save logic here
        pass

# Further refine saving and handling based on your project's models and database schema
