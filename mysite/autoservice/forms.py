from django import forms
from .models import Order
from django.contrib.auth.models import User

class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'deadline', 'status']
        widgets = {'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'},
                                                   format='%Y-%m-%dT%H:%M')}

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']