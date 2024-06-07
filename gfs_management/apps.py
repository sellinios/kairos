from django.apps import AppConfig

class GfsManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gfs_management'

    def ready(self):
        from . import tasks  # This should import tasks.py
