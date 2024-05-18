import os
import logging
import re
import cfgrib
import pandas as pd
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_grib_file(file_path):
    """Loads data from a GRIB file with all step types."""
    step_types = ['instant', 'avg', 'accum']
    datasets = []
    for step_type in step_types:
        try:
            ds = cfgrib.open_dataset(file_path, filter_by_keys={'stepType': step_type}, backend_kwargs={"indexpath": ""})
            logging.info(f"Successfully loaded data with stepType {step_type} from file {file_path}")
            datasets.append(ds)
        except Exception as e:
            logging.error(f"Failed to load data from file {file_path} with stepType {step_type}: {e}")
    return datasets

def extract_time_from_filename(filename):
    """Extract base datetime and forecast hour from the filename."""
    match = re.search(r'gfs\.t(\d{2})z\.pgrb2\.0p25\.f(\d{3})', filename)
    if not match:
        logging.error(f"Filename format not recognized: {filename}")
        return None

    cycle_hour = int(match.group(1))
    forecast_hour = int(match.group(2))

    now = datetime.now()
    base_date = datetime(now.year, now.month, now.day, cycle_hour)

    forecast_datetime = base_date + timedelta(hours=forecast_hour)
    return forecast_datetime

def consolidate_grib_data(grib2_folder, output_csv_path):
    """Consolidate data from all GRIB files into a single CSV."""
    all_data = []

    for filename in os.listdir(grib2_folder):
        if filename.endswith(".grib2"):
            file_path = os.path.join(grib2_folder, filename)
            datasets = load_grib_file(file_path)

            if not datasets:
                continue

            forecast_time = extract_time_from_filename(filename)
            if not forecast_time:
                continue

            for ds in datasets:
                for var_name in ds.data_vars:
                    data = ds[var_name].to_dataframe().reset_index()
                    data['forecast_time'] = forecast_time
                    data['variable'] = var_name
                    all_data.append(data)

    # Combine all data into a single DataFrame
    consolidated_data = pd.concat(all_data, ignore_index=True)

    # Save to CSV
    consolidated_data.to_csv(output_csv_path, index=False)
    logging.info(f"Data consolidated into {output_csv_path}")

class Command(BaseCommand):
    help = 'Consolidate GRIB data into a single CSV file'

    def handle(self, *args, **kwargs):
        grib2_folder = 'GFS/grib2_files/'
        output_csv_path = 'GFS/consolidated_forecasts.csv'

        consolidate_grib_data(grib2_folder, output_csv_path)
        logging.info("All tasks completed successfully.")
