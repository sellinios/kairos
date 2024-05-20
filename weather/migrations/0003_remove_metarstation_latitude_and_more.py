# migrations/0003_remove_metarstation_latitude_and_more.py

import django.contrib.gis.db.models.fields
from django.db import migrations, models
from django.contrib.gis.geos import Point

class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_alter_gfsforecast_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metarstation',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='metarstation',
            name='longitude',
        ),
        migrations.AddField(
            model_name='metarstation',
            name='code',
            field=models.CharField(default='TEMP_CODE', max_length=10),  # Use a temporary default code
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metarstation',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=Point(0, 0), geography=True, srid=4326),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='metarstation',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
