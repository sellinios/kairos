import logging
from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)

@shared_task
def cleanup_old_gfs_data_task():
    logger.info("Starting the cleanup of old GFS data.")
    call_command('gfs_data_cleanup')
    logger.info("Cleanup of old GFS data completed.")

@shared_task
def download_gfs_data_task(base_url="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod", dry_run=False):
    logger.info("Starting the GFS data download process.")
    call_command('gfs_data_download', base_url=base_url, dry_run=dry_run)
    logger.info("GFS data download process completed.")

@shared_task
def delete_tmp_files_task():
    logger.info("Starting the deletion of .tmp files.")
    call_command('gfs_data_cleanup_tmp')
    logger.info("Deletion of .tmp files completed.")
