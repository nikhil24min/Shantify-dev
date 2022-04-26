from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField

from django.forms import ModelForm
from django import forms

from .models import *

class UserRegisterForm(UserCreationForm):
    # email = EmailField(label=("Email address"), required=True,help_text=("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class GUProfilefForm(ModelForm):
    class Meta:
        model = GUprofile
        fields = '__all__'
        exclude = ['user','guOTP']
        readonly = ['country']
        widgets = {
        'dob': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
        }

