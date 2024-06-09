# backend/management/commands/migrate_safe.py
import logging
from django.core.management import BaseCommand, call_command
from django.db import OperationalError
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Applies migrations to the primary database and then to the backup database if successful'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Applying migrations to the primary database...')
            call_command('migrate', database='default')
            self.stdout.write(self.style.SUCCESS('Primary database migrations applied successfully.'))

            self.stdout.write('Applying migrations to the backup database...')
            call_command('migrate', database='backup')
            self.stdout.write(self.style.SUCCESS('Backup database migrations applied successfully.'))
        except OperationalError as e:
            error_message = f'Error applying migrations: {e}'
            self.stdout.write(self.style.ERROR(error_message))
            self.stdout.write(self.style.ERROR('Migrations to the backup database will not be applied.'))

            # Log the error
            logger.error(error_message)

            # Send an email notification
            send_mail(
                'Migration Failure Alert',
                error_message,
                'your_email@example.com',
                ['admin@example.com'],
                fail_silently=False,
            )
