"""
Model definition for GeographicCategory.
"""

from django.db import models

class GeographicCategory(models.Model):
    """Model representing a geographic category."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Geographic Category"
        verbose_name_plural = "Geographic Categories"

    def __str__(self):
        return self.name
