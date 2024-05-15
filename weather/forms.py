from django import forms
from .models import GFSForecast

class GFSForecastForm(forms.ModelForm):
    class Meta:
        model = GFSForecast
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GFSForecastForm, self).__init__(*args, **kwargs)
