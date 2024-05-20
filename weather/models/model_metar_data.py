import re
import datetime
from django.db import models
from .model_metar_station import MetarStation

class MetarData(models.Model):
    station = models.ForeignKey(
        MetarStation, on_delete=models.CASCADE, related_name='metar_data'
    )
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
            self.metar_timestamp = datetime.datetime(
                year=current_year, month=current_month, day=day, hour=hour, minute=minute
            )
        super(MetarData, self).save(*args, **kwargs)
