from django.db import models
from geography.models import Place

class GFSForecast(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)  # Temperature in Celsius
    precipitation = models.FloatField(null=True, blank=True)  # Precipitation in mm
    wind_speed = models.FloatField(null=True, blank=True)  # Wind speed in m/s
    specific_humidity = models.FloatField(null=True, blank=True)
    dew_point = models.FloatField(null=True, blank=True)  # Dew point in Celsius
    relative_humidity = models.FloatField(null=True, blank=True)  # Relative humidity in percentage
    apparent_temperature = models.FloatField(null=True, blank=True)  # Apparent temperature in Celsius
    max_temperature = models.FloatField(null=True, blank=True)  # Max temperature in Celsius
    min_temperature = models.FloatField(null=True, blank=True)  # Min temperature in Celsius
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Forecast for {self.place.name} at {self.timestamp}"


class MetarStation(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.longitude}, {self.latitude})"


class MetarData(models.Model):
    station = models.ForeignKey(MetarStation, on_delete=models.CASCADE, related_name='metar_data')
    metar_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Original timestamp when the record is added
    metar_timestamp = models.DateTimeField(null=True, blank=True)  # Actual timestamp from METAR text

    class Meta:
        ordering = ['-metar_timestamp']

    def __str__(self):
        return f"METAR Data for {self.station.name} at {self.timestamp}"

    def save(self, *args, **kwargs):
        # Extract date and time from metar_text
        # METAR reports typically start with the station code followed by the date and time of report as 'DDHHMMZ'
        metar_date_time_match = re.search(r'\b\d{6}Z\b', self.metar_text)
        if metar_date_time_match:
            metar_date_time_str = metar_date_time_match.group(0)
            # Parse the date and time assuming current month and year - adjust as needed
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            day = int(metar_date_time_str[:2])
            hour = int(metar_date_time_str[2:4])
            minute = int(metar_date_time_str[4:6])
            # Construct a datetime object
            self.metar_timestamp = datetime.datetime(year=current_year, month=current_month, day=day, hour=hour, minute=minute)

        super(MetarData, self).save(*args, **kwargs)