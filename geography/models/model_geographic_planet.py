"""
This module defines the GeographicPlanet model, which represents a planet and its attributes.
"""

from django.db import models

class GeographicPlanet(models.Model):
    """
    Represents a planet and its attributes.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Assuming planet names are unique
    mass = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    radius = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Geographic Planet"
        verbose_name_plural = "Geographic Planets"

    def __str__(self):
        """
        Return a string representation of the GeographicPlanet instance.
        """
        return str(self.name)
