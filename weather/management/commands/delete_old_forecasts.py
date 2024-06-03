from django.core.management.base import BaseCommand
from weather.models.model_gfs_forecast import GFSForecast
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete GFSForecast entries older than the current UTC hour'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        cutoff = now.replace(minute=0, second=0, microsecond=0)
        old_forecasts = GFSForecast.objects.filter(timestamp__lt=cutoff)
        count = old_forecasts.count()
        old_forecasts.delete()
        self.stdout.write(f'Deleted {count} old GFS forecasts.')
