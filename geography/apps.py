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

    def ready(self):
        # Import the signal handlers to connect them
        import geography.signals  # pylint: disable=import-outside-toplevel, unused-import
