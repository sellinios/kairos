# weather/signal.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import connection
from .models.model_gfs_forecast import GFSForecast

@receiver(post_delete, sender=GFSForecast)
def reset_forecast_sequence(sender, instance, **kwargs):
    """Reset the sequence for the primary key after all forecasts are deleted."""
    if not GFSForecast.objects.exists():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('weather_gfsforecast', 'id'), 1, false)"
            )
