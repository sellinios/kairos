import os
import logging
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPECTED_HOURS_0_120 = set(range(0, 121))
EXPECTED_HOURS_123_384 = set(range(123, 385, 3))
EXPECTED_FILE_COUNT = len(EXPECTED_HOURS_0_120) + len(EXPECTED_HOURS_123_384)

def is_directory_complete(directory):
    grib_files = {int(file.split('_')[-1].split('.')[0]) for file in os.listdir(directory) if file.endswith('.grib2')}
    return (EXPECTED_HOURS_0_120 | EXPECTED_HOURS_123_384).issubset(grib_files)

def combine_grib_files(directory, output_file):
    temp_output_file = output_file + ".tmp"
    grib_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.grib2')])

    with open(temp_output_file, 'wb') as wfd:
        for f in grib_files:
            with open(f, 'rb') as fd:
                wfd.write(fd.read())

    os.rename(temp_output_file, output_file)
    logger.info("Combined %d GRIB files into %s", len(grib_files), output_file)

class Command(BaseCommand):
    help = 'Combine GFS data files from complete folders into a single file'

    def handle(self, *args, **options):
        base_directory = "data"
        combined_directory = os.path.join(base_directory, "combined_data")

        if not os.path.exists(combined_directory):
            os.makedirs(combined_directory)

        combined_files_exist = all(
            os.path.exists(os.path.join(combined_directory, f"combined_{subdir}.grib2"))
            for subdir in os.listdir(base_directory)
            if os.path.isdir(os.path.join(base_directory, subdir)) and subdir != "combined_data"
        )

        if combined_files_exist:
            logger.info("All combined files already exist. No further action needed.")
            return

        for subdir in os.listdir(base_directory):
            full_path = os.path.join(base_directory, subdir)
            if os.path.isdir(full_path) and subdir != "combined_data":
                if is_directory_complete(full_path):
                    output_file = os.path.join(combined_directory, f"combined_{subdir}.grib2")
                    if not os.path.exists(output_file):
                        combine_grib_files(full_path, output_file)
                    else:
                        logger.info("Combined file already exists: %s", output_file)
                else:
                    logger.warning("Directory is incomplete: %s", full_path)

        logger.info("GFS data combining process completed.")
