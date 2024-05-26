import logging
import os
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from geography.models import Country
from gfs_management.models import GFSConfig, GFSParameter
from gfs_management.utils import download_gfs_data_sequence, parse_and_import_gfs_data, extract_grib_parameters

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

        now = datetime.utcnow().replace(tzinfo=timezone.utc)
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
