# geography/models/model_geographic_country.py

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.text import slugify
from .model_geographic_continent import Continent

class Country(models.Model):
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

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
