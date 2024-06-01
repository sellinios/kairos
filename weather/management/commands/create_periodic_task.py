# weather/management/commands/create_periodic_task.py

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Create periodic task for deleting old forecasts'

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )

        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Delete old GFS forecasts',
            task='weather.tasks.delete_old_forecasts',
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created periodic task'))
        else:
            self.stdout.write(self.style.WARNING('Periodic task already exists'))
