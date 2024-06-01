"""
This module defines the GeographicCountry model, which represents a country and its attributes.
"""

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.text import slugify
from .model_geographic_continent import GeographicContinent

class GeographicCountry(models.Model):
    """
    Represents a country and its attributes.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True)
    iso_alpha2 = models.CharField(max_length=2, blank=True, unique=True)
    iso_alpha3 = models.CharField(max_length=3, blank=True, unique=True)
    iso_numeric = models.IntegerField(blank=True, null=True, unique=True)
    continent = models.ForeignKey(GeographicContinent, on_delete=models.CASCADE, related_name='countries')
    area = models.FloatField(null=True)
    capital = models.CharField(max_length=100, null=True, blank=True)
    official_languages = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    geom = gis_models.MultiPolygonField(null=True, blank=True)
    fetch_forecasts = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Geographic Country"
        verbose_name_plural = "Geographic Countries"

    def save(self, *args, **kwargs):
        """
        Save the GeographicCountry instance, generating a slug if not already provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the GeographicCountry instance.
        """
        return str(self.name)

class GeographicCountryDetails(models.Model):
    """
    Represents additional details about a country.
    """
    population = models.IntegerField()
    country = models.OneToOneField(GeographicCountry, on_delete=models.CASCADE, related_name='details')

    def __str__(self):
        """
        Return a string representation of the GeographicCountryDetails instance.
        """
        return f"{self.country.name}: {self.population}"
