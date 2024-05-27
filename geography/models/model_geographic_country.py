"""
This module defines the Country model, which represents a country and its attributes.
"""

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.text import slugify
from .model_geographic_continent import Continent

class Country(models.Model):
    """
    Represents a country and its attributes.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True)  # Do not add the unique constraint for now
    iso_alpha2 = models.CharField(max_length=2, blank=True, unique=True)
    iso_alpha3 = models.CharField(max_length=3, blank=True, unique=True)
    iso_numeric = models.IntegerField(blank=True, null=True, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name='countries')
    area = models.FloatField(null=True)
    capital = models.CharField(max_length=100, null=True, blank=True)
    official_languages = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    geom = gis_models.MultiPolygonField(null=True, blank=True)
    fetch_forecasts = models.BooleanField(default=False)  # New field to enable forecasts

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def save(self, *args, **kwargs):
        """
        Save the Country instance, generating a slug if not already provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the Country instance.
        """
        return str(self.name)

class CountryDetails(models.Model):
    """
    Represents additional details about a country.
    """
    population = models.IntegerField()
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='details')

    def __str__(self):
        """
        Return a string representation of the CountryDetails instance.
        """
        return f"{self.country.name}: {self.population}"
