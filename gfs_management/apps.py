"""
App configuration for GFS management.
"""

from django.apps import AppConfig

class GfsManagementConfig(AppConfig):
    """
    GFS management application configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gfs_management'
