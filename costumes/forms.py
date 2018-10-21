from django import forms

from .models import *

class LoginForm(forms.Form):
    email = forms.CharField(label='email', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class CostumeForm(forms.ModelForm):
    class Meta:
        model = Costume
        fields = '__all__'

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = '__all__'
