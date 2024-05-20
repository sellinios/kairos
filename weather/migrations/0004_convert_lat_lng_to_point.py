# migrations/0004_convert_lat_lng_to_point.py

from django.db import migrations
from django.contrib.gis.geos import Point

def combine_lat_lng_to_point(apps, schema_editor):
    MetarStation = apps.get_model('weather', 'MetarStation')
    for station in MetarStation.objects.all():
        if hasattr(station, 'latitude') and hasattr(station, 'longitude'):
            station.location = Point(station.longitude, station.latitude)
            station.save()

class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_remove_metarstation_latitude_and_more'),
    ]

    operations = [
        migrations.RunPython(combine_lat_lng_to_point),
    ]
