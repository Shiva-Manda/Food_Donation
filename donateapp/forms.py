from django import forms
from .models import FoodAcceptor
from .models import FoodDonare

class FoodRequestForm(forms.ModelForm):
    
    class Meta:
        model = FoodAcceptor
        fields = ['contact_number', 'any_message']

class FoodDonareForm(forms.ModelForm):
    class Meta:
        model = FoodDonare
        fields = ['contact_number', 'address', 'food_details']

