from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import GeographicPlace

@receiver(post_delete, sender=GeographicPlace)
def reorder_places(sender, instance, **kwargs):
    """Reorder places and reset the sequence for the primary key after a place is deleted."""
    with transaction.atomic():
        places = GeographicPlace.objects.order_by('id')
        for index, place in enumerate(places, start=1):
            if place.id != index:
                GeographicPlace.objects.filter(id=place.id).update(id=index)

        # Reset the sequence for the primary key
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('geography_geographicplace', 'id'), "
                "(SELECT MAX(id) FROM geography_geographicplace))"
            )
