"""
This module defines models related to geographic administrative divisions.
"""

from django.db import models
from django.utils.text import slugify
from .model_geographic_country import GeographicCountry
from .model_geographic_level import GeographicLevel  # Import Level from model_geographic_level.py

class GeographicDivision(models.Model):
    """
    Represents an instance of an administrative division.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    level = models.ForeignKey(
        GeographicLevel, on_delete=models.CASCADE, related_name='divisions'
    )
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subdivisions'
    )
    country = models.ForeignKey(
        GeographicCountry, null=True, blank=True, on_delete=models.CASCADE, related_name='admin_divisions'
    )

    class Meta:
        verbose_name = "Geographic Division"
        verbose_name_plural = "Geographic Divisions"

    def __str__(self):
        return f"{self.name} ({self.level.name})"

    def save(self, *args, **kwargs):
        """
        Custom save method to set the slug if not provided and ensure uniqueness.
        """
        if not self.slug:
            self.slug = slugify(self.name)
            similar_slugs = GeographicDivision.objects.filter(
                slug__startswith=self.slug
            ).exclude(id=self.id).count()
            if similar_slugs > 0:
                self.slug = f"{self.slug}-{similar_slugs + 1}"
        super().save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the full name of the division.
        """
        return self.name
