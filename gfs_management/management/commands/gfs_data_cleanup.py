import logging
import os
import shutil
from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_directory = "data"
forecast_hours_0_120 = list(range(0, 121, 1))
forecast_hours_120_384 = list(range(123, 385, 3))
forecast_hours = forecast_hours_0_120 + forecast_hours_120_384
expected_file_count = len(forecast_hours)

def get_latest_4_cycles():
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    cycles = ['00', '06', '12', '18']
    latest_cycles = []

    for i in range(24):  # Check the last 24 hours
        cycle_time = now - timedelta(hours=i)
        date = cycle_time.strftime("%Y%m%d")
        hour = cycle_time.strftime("%H")
        if hour in cycles and (date, hour) not in latest_cycles:
            latest_cycles.append((date, hour))
        if len(latest_cycles) == 4:
            break

    return latest_cycles

def cleanup_old_gfs_data():
    latest_cycles = get_latest_4_cycles()
    latest_cycle_folders = {f"{date}_{hour}" for date, hour in latest_cycles}

    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path) and folder_name not in latest_cycle_folders:
            shutil.rmtree(folder_path)
            logger.info("Deleted old folder: %s", folder_path)

class Command(BaseCommand):
    help = 'Clean up old GFS data folders'

    def handle(self, *args, **kwargs):
        logger.info("Starting cleanup of old GFS data.")
        cleanup_old_gfs_data()
        logger.info("Cleanup of old GFS data completed.")
