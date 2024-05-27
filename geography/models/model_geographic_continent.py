"""
This module defines the Continent model, which represents a continent and its attributes.
"""

from django.db import models
from django.utils.text import slugify

class Continent(models.Model):
    """
    Represents a continent and its attributes.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Continent"
        verbose_name_plural = "Continents"

    def save(self, *args, **kwargs):
        """
        Save the Continent instance, generating a slug if not already provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Use Python 3 style super()

    def __str__(self):
        """
        Return a string representation of the Continent instance.
        """
        return str(self.name)

    def get_slug(self):
        """
        Return the slug of the Continent instance.
        """
        return self.slug
