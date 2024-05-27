"""
This module defines the MetarData model, which represents METAR weather data.
"""

import re
import datetime
from django.db import models
from .model_metar_station import MetarStation

class MetarData(models.Model):
    """
    Represents METAR weather data for a specific station.
    """
    station = models.ForeignKey(
        MetarStation, on_delete=models.CASCADE, related_name='metar_data'
    )
    metar_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metar_timestamp = models.DateTimeField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    conditions = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-metar_timestamp']

    def __str__(self):
        return f"METAR Data for {self.station.name} at {self.timestamp}"

    def save(self, *args, **kwargs):
        """
        Save the MetarData instance, decoding the METAR text before saving.
        """
        self.decode_metar()
        super().save(*args, **kwargs)

    def decode_metar(self):
        """
        Decode the METAR text to extract weather data attributes.
        """
        # Decode the METAR timestamp
        metar_date_time_match = re.search(r'\b\d{6}Z\b', self.metar_text)
        if metar_date_time_match:
            metar_date_time_str = metar_date_time_match.group(0)
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            day = int(metar_date_time_str[:2])
            hour = int(metar_date_time_str[2:4])
            minute = int(metar_date_time_str[4:6])
            self.metar_timestamp = datetime.datetime(
                year=current_year, month=current_month, day=day, hour=hour, minute=minute, tzinfo=datetime.timezone.utc
            )

        # Decode the temperature
        temp_match = re.search(r'\b(M?\d{2})\/(M?\d{2})\b', self.metar_text)
        if temp_match:
            temp_str = temp_match.group(1)
            temp = int(temp_str.replace('M', '-'))
            self.temperature = temp

        # Decode the wind speed
        wind_match = re.search(r'\b(\d{3})(\d{2})KT\b', self.metar_text)
        if wind_match:
            wind_speed_str = wind_match.group(2)
            wind_speed = int(wind_speed_str) * 1.852  # Convert from knots to km/h
            self.wind_speed = wind_speed

        # Decode the conditions
        if 'CAVOK' in self.metar_text:
            self.conditions = 'Clear'
        else:
            sky_condition_match = re.search(r'\b(SCT|BKN|OVC)(\d{3})\b', self.metar_text)
            if sky_condition_match:
                condition_code = sky_condition_match.group(1)
                conditions_map = {
                    'SCT': 'Partly Cloudy',
                    'BKN': 'Mostly Cloudy',
                    'OVC': 'Overcast'
                }
                self.conditions = conditions_map.get(condition_code, '')

            weather_phenomena_match = re.search(r'\b(-|\+)?(RA|SN|TS|DZ|FG|BR)\b', self.metar_text)
            if weather_phenomena_match:
                intensity = weather_phenomena_match.group(1) or ''
                phenomena = weather_phenomena_match.group(2)
                phenomena_map = {
                    'RA': 'Rain',
                    'SN': 'Snow',
                    'TS': 'Thunderstorm',
                    'DZ': 'Drizzle',
                    'FG': 'Fog',
                    'BR': 'Mist'
                }
                self.conditions = f"{intensity}{phenomena_map.get(phenomena, '')}".strip()
