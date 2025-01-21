from django import forms
from system.models import Location



class LocationForm(forms.Form):
    locationName = forms.CharField(max_length=50)
    locationAddress = forms.CharField(max_length=100)
    locationLat = forms.FloatField()
    locationLong = forms.FloatField()