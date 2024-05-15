from django.core.management.base import BaseCommand
import xarray as xr
import matplotlib.pyplot as plt
import os


class Command(BaseCommand):
    help = 'Visualize Total Precipitation for Greece region for all forecast hours'

    def handle(self, *args, **kwargs):
        grib2_dir = './grib2_files'
        if not os.path.exists(grib2_dir):
            self.stdout.write(self.style.ERROR(f'Directory not found: {grib2_dir}'))
            return

        for forecast_interval in range(0, 12, 1):
            output_file = os.path.join(grib2_dir, f'gfs.t18z.pgrb2.0p25.f{forecast_interval:03d}.nc')
            if not os.path.isfile(output_file):
                self.stdout.write(self.style.ERROR(f'File not found: {output_file}'))
                self.stdout.write(self.style.ERROR('Ensure the file is correctly downloaded and located in the specified directory.'))
                continue

            self.stdout.write(self.style.SUCCESS(f'Reading data from {output_file}'))
            self.visualize_tp(output_file, forecast_interval)

    def visualize_tp(self, file_path, forecast_interval):
        ds = xr.open_dataset(file_path)
        self.stdout.write(self.style.SUCCESS('Dataset loaded successfully'))

        # Print the available latitude and longitude ranges
        self.stdout.write(self.style.SUCCESS(f'Latitude range: {ds.latitude.values.min()} to {ds.latitude.values.max()}'))
        self.stdout.write(self.style.SUCCESS(f'Longitude range: {ds.longitude.values.min()} to {ds.longitude.values.max()}'))

        # Define the correct bounding box for Greece and surrounding area
        lat_bounds = slice(45, 30)  # Corrected latitude range
        lon_bounds = slice(15, 35)  # Corrected longitude range

        # Check available data variables
        self.stdout.write(self.style.SUCCESS(f'Available data variables: {list(ds.data_vars)}'))

        # Select the total precipitation variable and print summary
        if 'tp' in ds.data_vars:
            tp = ds['tp']
            self.stdout.write(self.style.SUCCESS(f'Total Precipitation data shape: {tp.shape}'))
            self.stdout.write(self.style.SUCCESS(f'Total Precipitation data summary: {tp}'))

            # Subset the data for the Greece region
            tp_region = tp.sel(latitude=lat_bounds, longitude=lon_bounds)
            self.stdout.write(self.style.SUCCESS(f'Subset Total Precipitation data shape: {tp_region.shape}'))

            # Print the first few values of the subset data for diagnostics
            self.stdout.write(self.style.SUCCESS(f'Subset Total Precipitation data values: {tp_region.values[:10]}'))

            # Check for missing values
            if tp_region.isnull().all():
                self.stdout.write(self.style.ERROR('Total Precipitation data for the selected region contains only missing values.'))
                return

            plt.figure(figsize=(10, 5))
            tp_region.plot()
            plt.title(f'Total Precipitation for Greece Region - Forecast Hour {forecast_interval:03d}')

            # Save the plot to a file
            plot_file = os.path.abspath(f'total_precipitation_greece_{forecast_interval:03d}.png')
            plt.savefig(plot_file)
            self.stdout.write(self.style.SUCCESS(f'Total precipitation plot for Greece saved as {plot_file}'))

            # Uncomment the following line if you want to also display the plot interactively
            # plt.show()
        else:
            self.stdout.write(self.style.ERROR('Total Precipitation (tp) variable not found in the dataset.'))
