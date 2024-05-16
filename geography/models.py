from django.db import models
import math

# Define the PlaceManager to include the nearest_place method
class PlaceManager(models.Manager):
    def nearest_place(self, current_latitude, current_longitude):
        """Find the nearest place to the given latitude and longitude."""
        R = 6371000  # Radius of the Earth in meters
        lat1 = math.radians(current_latitude)
        lon1 = math.radians(current_longitude)
        nearest_place = None
        smallest_distance = None

        for place in self.get_queryset():
            if place.latitude is not None and place.longitude is not None:
                lat2 = math.radians(float(place.latitude))
                lon2 = math.radians(float(place.longitude))
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c

                if smallest_distance is None or distance < smallest_distance:
                    smallest_distance = distance
                    nearest_place = place

        return nearest_place

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RegionalUnit(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='regional_units')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    regional_unit = models.ForeignKey(RegionalUnit, on_delete=models.CASCADE, related_name='municipalities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Counter(models.Model):
    last_assigned_number = models.IntegerField(default=0)

class Place(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=100)
    custom_id = models.IntegerField(unique=True, blank=True, null=True)  # Secondary index for display purposes
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    objects = PlaceManager()  # Use the custom manager for Place

    def __str__(self):
        return f"{self.name} (Custom ID: {self.custom_id})"

    def save(self, *args, **kwargs):
        if not self.custom_id:
            counter, _ = Counter.objects.get_or_create(pk=1)
            counter.last_assigned_number += 1
            counter.save()
            self.custom_id = counter.last_assigned_number
        super(Place, self).save(*args, **kwargs)