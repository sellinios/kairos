import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deploy the application'

    def handle(self, *args, **kwargs):
        FRONTEND_DIR = os.path.expanduser('~/kairos/frontend')
        MAIN_PROJECT_DIR = os.path.expanduser('~/kairos')

        # Update and upgrade system packages
        self.stdout.write(self.style.SUCCESS("Updating and upgrading system packages..."))
        result = subprocess.run(["sudo", "apt", "update"], check=False)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR("Failed to update system packages."))
            return
        result = subprocess.run(["sudo", "apt", "upgrade", "-y"], check=False)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR("Failed to upgrade system packages."))
            return

        self.stdout.write(self.style.SUCCESS("System packages updated and upgraded successfully."))

        # Check if frontend directory exists
        if not os.path.isdir(FRONTEND_DIR):
            self.stdout.write(self.style.ERROR(f"Frontend directory {FRONTEND_DIR} does not exist. Exiting..."))
            return

        # Navigate to the frontend directory and run npm build
        os.chdir(FRONTEND_DIR)
        self.stdout.write(self.style.SUCCESS("Running npm build..."))
        result = subprocess.run(["npm", "run", "build"], check=False)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR("Failed to build with npm. Please check the error messages."))
            return

        self.stdout.write(self.style.SUCCESS("npm build successful. Preparing to manage Python dependencies..."))

        # Check if main project directory exists
        if not os.path.isdir(MAIN_PROJECT_DIR):
            self.stdout.write(self.style.ERROR(f"Main project directory {MAIN_PROJECT_DIR} does not exist. Exiting..."))
            return

        # Navigate back to the main project directory to run Django commands and handle Python dependencies
        os.chdir(MAIN_PROJECT_DIR)

        # Export current Python package dependencies
        self.stdout.write(self.style.SUCCESS("Exporting Python dependencies..."))
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        with open("requirements.txt", "w") as f:
            f.write(result.stdout)
        self.stdout.write(self.style.SUCCESS("Python dependencies listed in requirements.txt."))

        # Run manage.py collectstatic
        self.stdout.write(self.style.SUCCESS("Running manage.py collectstatic..."))
        result = subprocess.run(["python", "manage.py", "collectstatic", "--noinput"], check=False)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR("Failed to collect static files. Please check the error messages."))
            return

        self.stdout.write(self.style.SUCCESS("Static files collected successfully. Restarting Gunicorn and Nginx..."))

        # Restart Gunicorn
        result = subprocess.run(["sudo", "systemctl", "restart", "gunicorn"], check=False)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR("Failed to restart Gunicorn. Please check the error messages."))
            return
        self.stdout.write(self.style.SUCCESS("Gunicorn restarted successfully."))

        # Restart Nginx
        result = subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=False)
        if result.returncode != 0:
            self.stdout.write(self.style.ERROR("Failed to restart Nginx. Please check the error messages."))
            return
        self.stdout.write(self.style.SUCCESS("Nginx restarted successfully."))
