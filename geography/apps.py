"""
This module defines the configuration for the geography app.
"""

from django.apps import AppConfig

class GeographyConfig(AppConfig):
    """
    Configuration class for the geography app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geography'
