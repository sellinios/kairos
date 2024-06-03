# weather/tasks.py

from celery import shared_task
from django.utils import timezone
from weather.models.model_gfs_forecast import GFSForecast

@shared_task
def delete_old_forecasts():
    now = timezone.now()
    cutoff = now.replace(minute=0, second=0, microsecond=0)
    old_forecasts = GFSForecast.objects.filter(timestamp__lt=cutoff)
    count = old_forecasts.count()
    old_forecasts.delete()
    return f'Deleted {count} old GFS forecasts.'
