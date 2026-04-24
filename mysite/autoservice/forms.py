from django import forms
from .models import Order

class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'deadline', 'status']
        widgets = {'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'},
                                                   format='%Y-%m-%dT%H:%M')}