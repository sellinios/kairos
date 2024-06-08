import subprocess
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check various aspects of Celery crontab setup'

    def handle(self, *args, **kwargs):
        self.check_celery_worker()
        self.check_celery_beat()
        self.inspect_celery_tasks()

    def check_celery_worker(self):
        self.stdout.write(self.style.SUCCESS('Checking Celery worker...'))
        try:
            result = subprocess.run(['celery', '-A', 'backend', 'status'], capture_output=True, text=True)
            logger.debug(f'Celery status output: {result.stdout}')
            if 'OK' in result.stdout:
                self.stdout.write(self.style.SUCCESS('Celery worker is running.'))
            else:
                self.stdout.write(self.style.ERROR('Celery worker is not responding.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error checking Celery worker: {e}'))

    def check_celery_beat(self):
        self.stdout.write(self.style.SUCCESS('Checking Celery beat...'))
        try:
            result = subprocess.run(['systemctl', 'is-active', '--quiet', 'celery-beat'], capture_output=True, text=True)
            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS('Celery beat is running.'))
            else:
                self.stdout.write(self.style.ERROR('Celery beat is not running.'))
                self.diagnose_celery_beat_issue()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error checking Celery beat: {e}'))

    def diagnose_celery_beat_issue(self):
        self.stdout.write(self.style.WARNING('Diagnosing Celery beat issue...'))
        try:
            result = subprocess.run(['systemctl', 'status', 'celery-beat'], capture_output=True, text=True)
            logger.debug(f'Celery beat status output: {result.stdout}')
            if result.returncode == 0:
                self.stdout.write(self.style.NOTICE(result.stdout))
            else:
                self.stdout.write(self.style.ERROR(result.stderr))

            journalctl_result = subprocess.run(['journalctl', '-u', 'celery-beat.service', '--no-pager'], capture_output=True, text=True)
            logger.debug(f'Journalctl output: {journalctl_result.stdout}')
            self.stdout.write(self.style.NOTICE('Celery Beat Service Logs:'))
            self.stdout.write(self.style.NOTICE(journalctl_result.stdout))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error diagnosing Celery beat: {e}'))

    def inspect_celery_tasks(self):
        self.stdout.write(self.style.SUCCESS('Inspecting Celery tasks...'))
        try:
            # Check registered tasks
            registered_tasks = subprocess.run(['celery', '-A', 'backend', 'inspect', 'registered'], capture_output=True, text=True)
            logger.debug(f'Registered tasks: {registered_tasks.stdout}')
            self.stdout.write(self.style.SUCCESS('Registered tasks:'))
            self.stdout.write(self.style.NOTICE(registered_tasks.stdout))

            # Check active tasks
            active_tasks = subprocess.run(['celery', '-A', 'backend', 'inspect', 'active'], capture_output=True, text=True)
            logger.debug(f'Active tasks: {active_tasks.stdout}')
            self.stdout.write(self.style.SUCCESS('Active tasks:'))
            self.stdout.write(self.style.NOTICE(active_tasks.stdout))

            # Check reserved tasks
            reserved_tasks = subprocess.run(['celery', '-A', 'backend', 'inspect', 'reserved'], capture_output=True, text=True)
            logger.debug(f'Reserved tasks: {reserved_tasks.stdout}')
            self.stdout.write(self.style.SUCCESS('Reserved tasks:'))
            self.stdout.write(self.style.NOTICE(reserved_tasks.stdout))

            # Check scheduled tasks
            scheduled_tasks = subprocess.run(['celery', '-A', 'backend', 'inspect', 'scheduled'], capture_output=True, text=True)
            logger.debug(f'Scheduled tasks: {scheduled_tasks.stdout}')
            self.stdout.write(self.style.SUCCESS('Scheduled tasks:'))
            self.stdout.write(self.style.NOTICE(scheduled_tasks.stdout))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error inspecting Celery tasks: {e}'))
