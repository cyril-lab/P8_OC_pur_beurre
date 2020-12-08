from django import forms
from django.core.validators import validate_email
from django.forms import PasswordInput


class CreateUserForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    surname = forms.CharField(label='surname', max_length=100)
    email = forms.EmailField(label='email', max_length=100)
    password1 = forms.CharField(label='password1', widget=PasswordInput())
    password2 = forms.CharField(label='password2', widget=PasswordInput())



