import re
import datetime
from geography.models import Place
from django.db import models
from django.utils import timezone
from geography.models import Place


class GFSForecast(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    forecast_data = models.JSONField()  # Can store more than one weather variable
    timestamp = models.DateTimeField(auto_now_add=False)

    def save(self, *args, **kwargs):
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.datetime.fromisoformat(self.timestamp)
            except ValueError:
                self.timestamp = timezone.now()
        elif not isinstance(self.timestamp, datetime.datetime):
            self.timestamp = timezone.now()
        super(GFSForecast, self).save(*args, **kwargs)

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
    timestamp = models.DateTimeField(auto_now_add=True)
    metar_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-metar_timestamp']

    def __str__(self):
        return f"METAR Data for {self.station.name} at {self.timestamp}"

    def save(self, *args, **kwargs):
        metar_date_time_match = re.search(r'\b\d{6}Z\b', self.metar_text)
        if metar_date_time_match:
            metar_date_time_str = metar_date_time_match.group(0)
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            day = int(metar_date_time_str[:2])
            hour = int(metar_date_time_str[2:4])
            minute = int(metar_date_time_str[4:6])
            self.metar_timestamp = datetime.datetime(year=current_year, month=current_month, day=day, hour=hour, minute=minute)

        super(MetarData, self).save(*args, **kwargs)
