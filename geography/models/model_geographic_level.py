from django.db import models

class Level(models.Model):
    name = models.CharField(max_length=100)
    level_order = models.IntegerField()
    country = models.ForeignKey('geography.Country', on_delete=models.CASCADE, related_name='levels')  # Use string reference to avoid circular import

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return self.name
