from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class RegisteringUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class AgencyRegistering(forms.ModelForm):
    class Meta:
        model = AgencyName
        fields = '__all__'


class UserExtendedForm(forms.ModelForm):
    class Meta:
        model = UserExtended
        fields = ['phone_number']


class GenerateQRCode(forms.ModelForm):
    class Meta:
        model = QRCodeGenerator
        fields = ['valid_until']
