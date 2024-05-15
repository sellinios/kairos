from django import forms
from .models import Place
from django.db.models import Min, Count

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.fields['custom_id'].initial = self.get_next_custom_id()

    def get_next_custom_id(self):
        if not Place.objects.exists():
            return 1
        # Get all used IDs sorted
        used_ids = Place.objects.order_by('custom_id').values_list('custom_id', flat=True)
        # Iterate to find the first gap
        expected_id = 1
        for used_id in used_ids:
            if used_id != expected_id:
                return expected_id
            expected_id += 1
        # If no gaps, return the next highest ID
        return expected_id
