"""
This module defines the GeographicContinent model, which represents a continent and its attributes.
"""

from django.db import models
from django.utils.text import slugify

class GeographicContinent(models.Model):
    """
    Model representing a continent and its attributes.

    Attributes:
        id (AutoField): Primary key for the model.
        name (CharField): Name of the continent.
        slug (SlugField): URL-friendly version of the continent name.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Geographic Continent"
        verbose_name_plural = "Geographic Continents"

    def save(self, *args, **kwargs):
        """
        Save the GeographicContinent instance, generating a slug if not already provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the GeographicContinent instance.
        """
        return str(self.name)

    def get_slug(self):
        """
        Return the slug of the GeographicContinent instance.
        """
        return self.slug
