import logging
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from weather.models import MetarStation, MetarData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetches and stores METAR data for each MetarStation, including past data.'

    def fetch_metar_data(self, station_code):
        # Modify the URL to fetch data for the past 48 hours
        url = f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={station_code}&hours=48&order=id%2C-obs&sep=true&format=html"
        logger.info(f"Fetching URL: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Successfully fetched the URL.")
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            # Extract multiple METAR data records
            metar_data_list = []
            for line in text.split('\n'):
                if 'Text:' in line:
                    metar_data = line.split('Text:')[1].strip()
                    metar_data_list.append(metar_data)

            if metar_data_list:
                logger.info("Successfully found the METAR data.")
                return metar_data_list
            else:
                logger.warning("No METAR data found.")
                return None
        else:
            logger.error(f"Failed to fetch the URL with status code: {response.status_code}")
            return None

    def save_metar_data(self, station, metar_data_list):
        for metar_data in metar_data_list:
            # Check for duplicate data
            if MetarData.objects.filter(station=station, metar_text=metar_data).exists():
                logger.info("Duplicate METAR data found. Skipping.")
                continue

            # Save new METAR data
            metar_record = MetarData(station=station, metar_text=metar_data)
            metar_record.save()
            logger.info(f"Saved METAR data for {station.name}")

            # Delete the oldest record if count exceeds 100
            while MetarData.objects.filter(station=station).count() > 100:
                oldest_record = MetarData.objects.filter(station=station).last()
                oldest_record.delete()
                logger.info(f"Deleted oldest METAR data for {station.name}")

    def handle(self, *args, **kwargs):
        for station in MetarStation.objects.all():
            logger.info(f"Processing station: {station.name}")
            metar_data_list = self.fetch_metar_data(station.name)
            if metar_data_list:
                for metar_data in metar_data_list:
                    self.stdout.write(f"METAR Data for {station.name}: {metar_data}")
                self.save_metar_data(station, metar_data_list)
            else:
                self.stdout.write(self.style.WARNING(f"No METAR data found for {station.name}"))

        logger.info("Done.")
