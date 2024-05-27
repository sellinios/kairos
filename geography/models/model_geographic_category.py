"""
This module defines the Category model, which represents a category of geographic entities.
"""

from django.db import models

class Category(models.Model):
    """
    Represents a category of geographic entities.
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Return a string representation of the Category instance.
        """
        return str(self.name)
