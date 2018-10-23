from django import forms

from .models import *

class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class CostumeForm(forms.ModelForm):
    class Meta:
        model = Costume
        fields = '__all__'

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = '__all__'

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='firs_name', max_length=50)
    last_name = forms.CharField(label='last_name', max_length=50)
    login = forms.CharField(label='login', max_length=50)
    email = forms.CharField(label='email', max_length=50)
    password = forms.CharField(label='password_1', max_length=50, min_length=6)
