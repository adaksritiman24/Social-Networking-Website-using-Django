from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Person

class Signupform(UserCreationForm):
    password1 = forms.CharField(label = 'Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label = 'Retype Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = Person
        fields = ['first_name','last_name','email','username','dob','accept']
        widgets={
            'dob': forms.DateInput(format = ('%d-%m-%y'),attrs={'class':'form-control', 'type': 'date'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'accept':forms.CheckboxInput(attrs={'class':'form-check-input','required':True}),
        }
        labels = {
            'dob':'Date of Birth'
        }
class LoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Username',widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label = 'Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))

    