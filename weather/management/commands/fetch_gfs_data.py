import os
import requests
import xarray as xr
from django.core.management.base import BaseCommand
from django.utils import timezone
import cfgrib
import numpy as np
from weather.models import GFSForecast
from geography.models import Place

class Command(BaseCommand):
    help = 'Fetch GFS data and process variables'

    def handle(self, *args, **kwargs):
        base_url = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs'
        now = timezone.now()

        # Calculate the GFS run (cycle) closest to current time
        forecast_hours = [0, 6, 12, 18]
        forecast_hour = max([hour for hour in forecast_hours if hour <= now.hour])

        # Get the closest available cycle
        date_str = now.strftime('%Y%m%d')
        cycle = f'{forecast_hour:02d}'

        # Directory to store the downloaded GRIB2 files
        grib2_dir = './grib2_files'
        os.makedirs(grib2_dir, exist_ok=True)

        for forecast_interval in range(0, 12, 1):  # Download every 1 hour up to 12 hours
            file_name = f'gfs.t{cycle}z.pgrb2.0p25.f{forecast_interval:03d}'
            file_url = f'{base_url}.{date_str}/{cycle}/atmos/{file_name}'
            local_file_path = os.path.join(grib2_dir, file_name)

            if not os.path.exists(local_file_path):
                self.stdout.write(f'Downloading {file_name}...')
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(local_file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    self.stderr.write(f'Failed to download {file_url}')
                    continue
            else:
                self.stdout.write(f'{file_name} already downloaded.')

            filters = [
                {'typeOfLevel': 'meanSea'},
                {'typeOfLevel': 'surface'},
                {'typeOfLevel': 'heightAboveGround', 'level': 2},  # Example for 2 meters above ground
                {'typeOfLevel': 'isobaricInhPa', 'level': 500},  # Example for 500 hPa level
            ]

            for filter_keys in filters:
                try:
                    self.stdout.write(f'\nUsing filter: {filter_keys}')
                    ds = xr.open_dataset(local_file_path, engine='cfgrib', filter_by_keys=filter_keys)
                    self.stdout.write(f'All Variables: {list(ds.variables.keys())}')
                    self.stdout.write(f'All Coordinates: {list(ds.coords.keys())}')
                    self.stdout.write(f'Attributes: {ds.attrs}')

                    # Example: Extracting temperature at 2 meters above ground
                    if 't2m' in ds.variables:
                        temp2m = ds['t2m'].values  # Assuming this is the temperature at 2 meters
                        times = ds['time'].values

                        # Convert numpy.datetime64 to string
                        times_str = [np.datetime_as_string(time, unit='h') for time in times]

                        # Find the nearest Place (for simplicity, this example assumes one Place)
                        place = Place.objects.first()
                        if place:
                            forecast_data = []
                            for time_str, temp in zip(times_str, temp2m):
                                forecast_data.append({
                                    'time': time_str,  # Use the converted string time
                                    'temp2m': temp.tolist()  # Convert numpy array to list
                                })

                            GFSForecast.objects.create(
                                place=place,
                                forecast_data=forecast_data,
                                timestamp=timezone.now()
                            )

                    # Save the dataset to a NetCDF file for further use
                    output_file = os.path.join(grib2_dir, f'{file_name}.nc')
                    os.chmod(output_file, 0o755)  # Ensure the file is writable
                    ds.to_netcdf(output_file)
                    self.stdout.write(f'Saved dataset to {output_file}')

                except cfgrib.dataset.DatasetBuildError as e:
                    self.stderr.write(self.style.ERROR(f"Error opening dataset with filter {filter_keys}: {e}"))
                except IndexError as e:
                    self.stderr.write(self.style.ERROR(f"IndexError with filter {filter_keys}: {e}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Unexpected error with filter {filter_keys}: {e}"))
