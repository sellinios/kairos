from django.db import models
from .model_geografic_continent import Continent

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    iso_alpha2 = models.CharField(max_length=2, blank=True, unique=True)  # ISO codes should be unique
    iso_alpha3 = models.CharField(max_length=3, blank=True, unique=True)
    iso_numeric = models.IntegerField(blank=True, null=True, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name='countries')
    area = models.FloatField(null=True)
    capital = models.CharField(max_length=100, null=True, blank=True)
    official_languages = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
