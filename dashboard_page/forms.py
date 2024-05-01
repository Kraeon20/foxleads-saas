from django import forms
from .models import StateData

class DashboardForm(forms.Form):
    state = forms.ModelChoiceField(queryset=StateData.objects.values_list('state', flat=True).distinct(), empty_label="Select State")
    city = forms.ModelChoiceField(queryset=StateData.objects.values_list('city', flat=True).distinct(), empty_label="Select City")
    area_code = forms.ModelChoiceField(queryset=StateData.objects.values_list('area_code', flat=True).distinct(), empty_label="Select Area Code")
