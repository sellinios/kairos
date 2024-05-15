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

        self.stdout.write("Starting GFS data fetch...")

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

                    place = Place.objects.first()
                    if place:
                        # Prepare forecast data for each time step
                        for time in ds['time'].values:
                            time_str = np.datetime_as_string(time, unit='h')
                            data_point = {'time': time_str}

                            # Extract relevant variables dynamically
                            if 't2m' in ds.variables:
                                data_point['temperature'] = ds['t2m'].sel(time=time).values.item()
                            if 'prate' in ds.variables:
                                data_point['precipitation'] = ds['prate'].sel(time=time).values.item()
                            if 'wind_speed' in ds.variables:
                                data_point['wind_speed'] = ds['wind_speed'].sel(time=time).values.item()

                            # Save the forecast data to the database
                            GFSForecast.objects.create(
                                place=place,
                                temperature=data_point.get('temperature'),
                                precipitation=data_point.get('precipitation'),
                                wind_speed=data_point.get('wind_speed'),
                                timestamp=time
                            )
                            self.stdout.write(f"Imported data for {place.name} at {time_str}")

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

        self.stdout.write(self.style.SUCCESS('Completed importing GFS data.'))
