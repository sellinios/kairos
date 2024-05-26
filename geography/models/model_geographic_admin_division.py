from django.db import models

class AdminDivisionInstance(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.ForeignKey('geography.Level', on_delete=models.CASCADE, related_name='divisions')  # Use string reference to avoid circular import
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subdivisions')

    class Meta:
        verbose_name = "Administrative Division Instance"
        verbose_name_plural = "Administrative Division Instances"

    def __str__(self):
        return f"{self.name} ({self.level.name})"

class AdministrativeConfiguration(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Administrative Configuration"
        verbose_name_plural = "Administrative Configurations"

    def __str__(self):
        return self.name
