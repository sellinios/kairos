# geography/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import transaction
from .models.model_geographic_place import Place

@receiver(post_delete, sender=Place)
def reorder_places(sender, instance, **kwargs):
    with transaction.atomic():
        places = Place.objects.order_by('id')
        for index, place in enumerate(places, start=1):
            if place.id != index:
                Place.objects.filter(id=place.id).update(id=index)

        # Reset the sequence for the primary key
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('geography_place', 'id'), (SELECT MAX(id) FROM geography_place))")
