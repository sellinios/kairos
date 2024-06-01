import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Manage migrations for custom apps'

    def handle(self, *args, **kwargs):
        custom_apps = ["api", "articles", "geography", "weather", "gfs_management"]
        builtin_apps = ["admin", "auth", "contenttypes", "sessions"]

        self.stdout.write(self.style.SUCCESS("Removing existing migrations for custom apps..."))

        for app in custom_apps:
            migrations_dir = os.path.join(app, "migrations")
            if os.path.exists(migrations_dir):
                for file in os.listdir(migrations_dir):
                    if file != "__init__.py":
                        os.remove(os.path.join(migrations_dir, file))
                with open(os.path.join(migrations_dir, "__init__.py"), 'w') as f:
                    pass
                self.stdout.write(self.style.SUCCESS(f"Cleaned migrations for {app}."))
            else:
                self.stdout.write(self.style.WARNING(f"Migrations directory for app {app} does not exist."))

        self.stdout.write(self.style.SUCCESS("Creating new initial migrations for geography..."))
        if subprocess.call(["python", "manage.py", "makemigrations", "geography"]) != 0:
            self.stdout.write(self.style.ERROR("Failed to create migrations for geography."))
            return

        self.stdout.write(self.style.SUCCESS("Creating new initial migrations for gfs_management..."))
        if subprocess.call(["python", "manage.py", "makemigrations", "gfs_management"]) != 0:
            self.stdout.write(self.style.ERROR("Failed to create migrations for gfs_management."))
            return

        self.stdout.write(self.style.SUCCESS("Creating new initial migrations for other apps..."))
        if subprocess.call(["python", "manage.py", "makemigrations", "articles", "weather"]) != 0:
            self.stdout.write(self.style.ERROR("Failed to create migrations for articles and weather."))
            return

        self.stdout.write(self.style.SUCCESS("Applying migrations..."))
        if subprocess.call(["python", "manage.py", "migrate"]) != 0:
            self.stdout.write(self.style.ERROR("Failed to apply migrations."))
            return

        self.stdout.write(self.style.SUCCESS("Migrations applied successfully."))
