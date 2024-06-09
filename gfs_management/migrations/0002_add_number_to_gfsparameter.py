# gfs_management/migrations/0002_add_number_to_gfsparameter.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gfs_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gfsparameter',
            name='number',
            field=models.IntegerField(unique=True, null=True),  # Use null=True temporarily to avoid issues with existing records
        ),
    ]
