from django.db import models
from geography.models import Country

class GFSParameter(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    level = models.BigIntegerField()
    type_of_level = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class GFSConfig(models.Model):
    countries = models.ManyToManyField(Country, related_name='gfs_configs')
    forecast_hours = models.CharField(max_length=255, default="24")  # Store as comma-separated values
    parameters = models.ManyToManyField(GFSParameter, blank=True)

    def __str__(self):
        return ', '.join(country.name for country in self.countries.all())

    def get_forecast_hours(self):
        # Convert the forecast_hours field to a list of integers
        hours = [int(hour) for hour in self.forecast_hours.split(',')]
        # If only one value is provided, expand it to a full range from 0 to that hour
        if len(hours) == 1:
            hours = list(range(hours[0] + 1))
        return hours
