from django import forms
from django.forms import ModelForm, DateInput, Form, PasswordInput

from .models import *

class LoginForm(Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class BorrowingForm(ModelForm):
    class Meta:
        model = Borrowing
        fields = '__all__'
        widgets = {
            'borrowed_date': DateInput(attrs={'type': 'date'}),
            'return_date': DateInput(attrs={'type': 'date'}),
        }

class CostumeTemplateForm(ModelForm):
    class Meta:
        model = CostumeTemplate
        fields = '__all__'

class CostumeForm(ModelForm):
    class Meta:
        model = Costume
        fields = '__all__'
        widgets = {
            'manufactured': DateInput(attrs={'type': 'date'}),
        }

class AccessoryForm(ModelForm):
    class Meta:
        model = Accessory
        fields = '__all__'
        widgets = {
            'manufactured': DateInput(attrs={'type': 'date'}),
        }

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

class RegisterForm(Form):
    first_name = forms.CharField(label='firs_name', max_length=50)
    last_name = forms.CharField(label='last_name', max_length=50)
    login = forms.CharField(label='login', max_length=50)
    email = forms.CharField(label='email', max_length=50)
    password = forms.CharField(label='password_1', max_length=50, min_length=6)

class EditManagerForm(Form):
    id = forms.CharField(label='id', max_length=50)
    first_name = forms.CharField(label='first_name', max_length=50, required=False)
    last_name = forms.CharField(label='last_name', max_length=50, required=False)
    email = forms.CharField(label='email', max_length=50, required=False)
    address = forms.CharField(label='address', max_length=50, required=False)
    tel_num = forms.CharField(label='tel_num', max_length=50, required=False)
    store = forms.CharField(label='store', max_length=50, required=False)
    super_manager = forms.CharField(label='super_manager', max_length=50, required=False)

class CreateManagerForm(Form):
    login = forms.CharField(label='login', max_length=50)
    password = forms.CharField(label='password', max_length=50)
    first_name = forms.CharField(label='first_name', max_length=50, required=False)
    last_name = forms.CharField(label='last_name', max_length=50, required=False)
    email = forms.CharField(label='email', max_length=50, required=False)
    address = forms.CharField(label='address', max_length=50, required=False)
    tel_num = forms.CharField(label='tel_num', max_length=50, required=False)
    store = forms.CharField(label='store', max_length=50, required=False)
    super_manager = forms.CharField(label='super_manager', max_length=50, required=False)

class EditEmployeeForm(Form):
    id = forms.CharField(label='id', max_length=50)
    first_name = forms.CharField(label='first_name', max_length=50, required=False)
    last_name = forms.CharField(label='last_name', max_length=50, required=False)
    email = forms.CharField(label='email', max_length=50, required=False)
    address = forms.CharField(label='address', max_length=50, required=False)
    tel_num = forms.CharField(label='tel_num', max_length=50, required=False)
    store = forms.CharField(label='store', max_length=50, required=False)

class CreateEmployeeForm(Form):
    login = forms.CharField(label='login', max_length=50)
    password = forms.CharField(label='password', max_length=50)
    first_name = forms.CharField(label='first_name', max_length=50, required=False)
    last_name = forms.CharField(label='last_name', max_length=50, required=False)
    email = forms.CharField(label='email', max_length=50, required=False)
    address = forms.CharField(label='address', max_length=50, required=False)
    tel_num = forms.CharField(label='tel_num', max_length=50, required=False)
    store = forms.CharField(label='store', max_length=50, required=False)
