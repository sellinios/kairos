from django.db import models
from .country import Country

class AdministrativeDivision(models.Model):
    ISO_ALPHA2_DETAILS = {
        'AR': ('Administrative Region', 'Attica'),
        'PR': ('Province', 'Some Province'),
        'DT': ('District', 'Some District'),
        'ST': ('State', 'Some State'),
        'CT': ('County', 'Some County'),
        'CN': ('Canton', 'Some Canton'),
        'RG': ('Region', 'Some Region'),
        'DP': ('Department', 'Some Department'),
        'MT': ('Municipality', 'Some Municipality'),
        'TP': ('Territory', 'Some Territory'),
        'BR': ('Borough', 'Some Borough'),
        'SD': ('Subdistrict', 'Some Subdistrict'),
        'VS': ('Village', 'Some Village'),
        'TL': ('Townland', 'Some Townland'),
        # Add more categories and names as needed
    }

    ISO_ALPHA3_DETAILS = {
        'ARR': ('Administrative Region', 'Attica'),
        'PRV': ('Province', 'Some Province'),
        'DIS': ('District', 'Some District'),
        'STA': ('State', 'Some State'),
        'COU': ('County', 'Some County'),
        'CAN': ('Canton', 'Some Canton'),
        'REG': ('Region', 'Some Region'),
        'DEP': ('Department', 'Some Department'),
        'MUN': ('Municipality', 'Some Municipality'),
        'TER': ('Territory', 'Some Territory'),
        'BOR': ('Borough', 'Some Borough'),
        'SUB': ('Subdistrict', 'Some Subdistrict'),
        'VIL': ('Village', 'Some Village'),
        'TWN': ('Townland', 'Some Townland'),
        # Add more categories and names as needed
    }

    ISO_NUMERIC_DETAILS = {
        1: ('Administrative Region', 'Attica'),
        2: ('Province', 'Some Province'),
        3: ('District', 'Some District'),
        4: ('State', 'Some State'),
        5: ('County', 'Some County'),
        6: ('Canton', 'Some Canton'),
        7: ('Region', 'Some Region'),
        8: ('Department', 'Some Department'),
        9: ('Municipality', 'Some Municipality'),
        10: ('Territory', 'Some Territory'),
        11: ('Borough', 'Some Borough'),
        12: ('Subdistrict', 'Some Subdistrict'),
        13: ('Village', 'Some Village'),
        14: ('Townland', 'Some Townland'),
        # Add more categories and names as needed
    }

    name = models.CharField(max_length=100)
    iso_alpha2 = models.CharField(
        max_length=3,
        blank=True,
        choices=[(key, f"{key} - {value[0]}") for key, value in ISO_ALPHA2_DETAILS.items()]
    )
    iso_alpha3 = models.CharField(
        max_length=3,
        blank=True,
        choices=[(key, f"{key} - {value[0]}") for key, value in ISO_ALPHA3_DETAILS.items()]
    )
    iso_numeric = models.IntegerField(
        blank=True,
        null=True,
        choices=[(key, f"{key} - {value[0]}") for key, value in ISO_NUMERIC_DETAILS.items()]
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    parent_division = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subdivisions')
    category = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Administrative Division"
        verbose_name_plural = "Administrative Divisions"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.iso_alpha2:
            self.category, self.name = self.ISO_ALPHA2_DETAILS.get(self.iso_alpha2, (self.category, self.name))
        if self.iso_alpha3:
            self.category, self.name = self.ISO_ALPHA3_DETAILS.get(self.iso_alpha3, (self.category, self.name))
        if self.iso_numeric:
            self.category, self.name = self.ISO_NUMERIC_DETAILS.get(self.iso_numeric, (self.category, self.name))
        super().save(*args, **kwargs)
