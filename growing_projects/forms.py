# growing_projects/forms.py
from django import forms
from .models import Crop

class GardenAddCropForm(forms.Form):
    crop = forms.ModelChoiceField(queryset=Crop.objects.all(), required=True, label='Select crop')