from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class RegisteringUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class AgencyRegistering(forms.ModelForm):
    class Meta:
        model = AgencyName
        fields = ['name', 'link', 'img', 'desc']


class UserExtendedForm(forms.ModelForm):
    class Meta:
        model = UserExtended
        fields = ['phone_number', 'identity_number']


class GenerateQRCodeForms(forms.ModelForm):
    class Meta:
        model = QRCodeGenerator
        fields = ['valid_until']

        widgets = {
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
