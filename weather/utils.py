from datetime import datetime, timedelta, timezone
import re


def extract_forecast_details_from_filename(filename):
    match = re.search(r'gfs_(\d{8})_(\d{2})_(\d{3})\.grib2', filename)
    if match:
        date_str = match.group(1)
        cycle_hour_str = match.group(2)
        forecast_hour_str = match.group(3)

        # Convert extracted strings to datetime and integers
        date = datetime.strptime(date_str, "%Y%m%d").replace(tzinfo=timezone.utc)
        cycle_hour = int(cycle_hour_str)
        forecast_hour = int(forecast_hour_str)

        # Calculate utc_cycle_time and valid_datetime
        utc_cycle_time = date + timedelta(hours=cycle_hour)
        valid_datetime = utc_cycle_time + timedelta(hours=forecast_hour)

        return valid_datetime, utc_cycle_time, forecast_hour
    return None, None, None
