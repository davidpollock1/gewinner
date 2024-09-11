from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser  # or your custom user model if you're using one
        fields = ['username', 'password1', 'password2']
        
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'phone_number': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'address': forms.TextInput(attrs={'class': 'input input-bordered'}),
        }