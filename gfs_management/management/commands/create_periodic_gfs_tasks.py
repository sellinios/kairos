# gfs_management/management/commands/create_periodic_gfs_tasks.py

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class Command(BaseCommand):
    help = 'Create periodic tasks for running GFS script'

    def handle(self, *args, **kwargs):
        schedules = [
            (5, 0, 'Run GFS Script for 00:00 UTC run'),
            (11, 0, 'Run GFS Script for 06:00 UTC run'),
            (17, 0, 'Run GFS Script for 12:00 UTC run'),
            (23, 0, 'Run GFS Script for 18:00 UTC run')
        ]

        for hour, minute, task_name in schedules:
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
            )
            PeriodicTask.objects.update_or_create(
                crontab=schedule,
                name=task_name,
                defaults={'task': 'gfs_management.tasks.run_gfs_script'},
            )

        self.stdout.write(self.style.SUCCESS('Successfully created/updated periodic tasks for running GFS script.'))
