"""
This module defines the MetarStation model, which represents a METAR weather station.
"""

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.gis.geos import Point
import requests

class MetarStation(models.Model):
    """
    Represents a METAR weather station.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)  # e.g., LGAV
    location = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)

    def __str__(self):
        """
        Return a string representation of the MetarStation.
        """
        return str(self.name)

    def update_location(self):
        """
        Update the location of the MetarStation using the Nominatim API.
        """
        url = f"https://nominatim.openstreetmap.org/search?q={self.name}&format=json&polygon=1&addressdetails=1"
        response = requests.get(url, timeout=10)  # Added timeout argument
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                self.location = Point(float(longitude), float(latitude), srid=4326)
                self.save()
                return True
        return False
