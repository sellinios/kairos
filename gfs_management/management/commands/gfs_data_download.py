from datetime import datetime, timedelta, timezone
import logging
import os
import requests
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_gfs_data_sequence(base_url, date, hour, forecast_hours, save_directory):
    os.makedirs(save_directory, exist_ok=True)
    grib_files = []

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
        else:
            logger.info("File already exists: %s", save_path)
            grib_files.append(save_path)
    return grib_files

class Command(BaseCommand):
    """
    Download GFS data into the specified folders.
    """

    help = 'Download GFS data into the specified folders'

    def add_arguments(self, parser):
        parser.add_argument('--base_url', type=str, default="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod")
        parser.add_argument('--date', type=str, default=None)
        parser.add_argument('--hours_to_try', nargs='+', type=str, default=['00', '06', '12', '18'])

    def handle(self, *args, **options):
        logger.info("Starting the GFS data download process.")

        base_url = options['base_url']
        if options['date']:
            date = options['date']
        else:
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
            date = now.strftime("%Y%m%d")

        hours_to_try = options['hours_to_try']

        def try_download(date, hours, forecast_hours):
            for hour in hours:
                save_directory = f"data/{date}_{hour}"
                if os.path.exists(save_directory):
                    logger.info("Directory already exists: %s, skipping download.", save_directory)
                    continue
                grib_files = download_gfs_data_sequence(base_url, date, hour, forecast_hours, save_directory)
                if grib_files:
                    return grib_files
            return None

        # Define the forecast hours
        forecast_hours_0_120 = list(range(0, 121, 1))
        forecast_hours_120_384 = list(range(123, 385, 3))
        forecast_hours = forecast_hours_0_120 + forecast_hours_120_384

        logger.info("Forecast hours: %s", forecast_hours)
        logger.info("Downloading GFS data for date: %s, hours: %s", date, hours_to_try)

        grib_files = try_download(date, hours_to_try, forecast_hours)
        if not grib_files:
            logger.warning("Download failed, trying previous cycle.")
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
            now -= timedelta(days=1)
            date = now.strftime("%Y%m%d")
            grib_files = try_download(date, hours_to_try, forecast_hours)
            if not grib_files:
                logger.error("Download failed again, aborting.")
                return

        logger.info("GFS data download process completed for date: %s", date)