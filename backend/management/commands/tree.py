import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generates a tree structure of the project'

    def handle(self, *args, **kwargs):
        try:
            result = subprocess.run(
                ["tree", "-L", "10", "-I", "node_modules|build|assets|venv|natural_earth_vector|data|__pycache__"],
                check=True,
                text=True,
                capture_output=True
            )
            self.stdout.write(self.style.SUCCESS(result.stdout))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Error generating project tree: {e}"))
