"""
This module defines models related to geographic administrative divisions.
"""

from django.db import models

class AdminDivisionInstance(models.Model):
    """
    Represents an instance of an administrative division.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.ForeignKey(
        'geography.Level',
        on_delete=models.CASCADE,
        related_name='divisions'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subdivisions'
    )

    class Meta:
        verbose_name = "Administrative Division Instance"
        verbose_name_plural = "Administrative Division Instances"

    def __str__(self):
        """
        Return a string representation of the AdminDivisionInstance.
        """
        return f"{self.name} ({self.level.name})"

    def get_full_name(self):
        """
        Return the full name of the AdminDivisionInstance.
        """
        return self.name


class AdministrativeConfiguration(models.Model):
    """
    Represents the configuration of an administrative division.
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Administrative Configuration"
        verbose_name_plural = "Administrative Configurations"

    def __str__(self):
        """
        Return a string representation of the AdministrativeConfiguration.
        """
        return str(self.name)

    def get_configuration_name(self):
        """
        Return the name of the administrative configuration.
        """
        return self.name
