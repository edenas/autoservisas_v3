from django import forms
from .models import Order

class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'deadline', 'status']
        widgets = {'deadline': forms.DateInput(attrs={'type': 'datetime-local'})}