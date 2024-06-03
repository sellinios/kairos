# gfs_management/tasks.py

from celery import shared_task
from django.core.management import call_command

@shared_task
def run_gfs_script():
    call_command('gfs')
