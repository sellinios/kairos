"""
This module defines the Level model, which represents administrative levels within a country.
"""

from django.db import models

class Level(models.Model):
    """
    Represents an administrative level within a country.
    """
    name = models.CharField(max_length=100)
    level_order = models.IntegerField()
    country = models.ForeignKey(
        'geography.Country',
        on_delete=models.CASCADE,
        related_name='levels'
    )  # Use string reference to avoid circular import

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        """
        Return a string representation of the Level instance.
        """
        return str(self.name)
