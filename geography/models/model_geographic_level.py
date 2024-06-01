"""
This module defines the GeographicLevel model, which represents administrative levels within a country.
"""

from django.db import models

class GeographicLevel(models.Model):
    """
    Represents an administrative level within a country.
    """
    name = models.CharField(max_length=100)
    level_order = models.IntegerField()
    country = models.ForeignKey(
        'geography.GeographicCountry',
        on_delete=models.CASCADE,
        related_name='levels'
    )  # Use string reference to avoid circular import

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        """
        Return a string representation of the GeographicLevel instance.
        """
        return str(self.name)
