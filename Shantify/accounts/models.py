from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

import datetime
import re

def validate_string(value):
    if re.match(r'^[A-Z a-z]*$', value):
        return True
    else:
        raise ValidationError('Only Alphabets are allowed')

def validate_mobile(value):
    if not value.isdigit():
        raise ValidationError('Mobile number should be a number')

    if len(str(value)) == 10:
        return value
    else:
        raise ValidationError('Mobile number should be 10 digits long.')


def validate_aadhar(value):
    if not value.isdigit():
        raise ValidationError('Aadhar number should be a number')

    if len(str(value)) == 12:
        return value
    else:
        raise ValidationError('Aadhar number should be 12 digits long.')


def validate_pan(value):
    if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
        return True
    else:
        raise ValidationError('This is not valid PAN number')

    if len(str(value)) == 10:
        return value
    else:
        raise ValidationError('PAN number should be 12 digits long.')


def validate_dob(value):
    dob = value
    age = (datetime.date.today() - dob).days/365
    if age < 18:
        raise ValidationError('Must be at least 18 years old to register')
    return value

class GUprofile(models.Model):

    COUNTRY_CHOICES =(('INDIA','INDIA'),)
    GENDER_CHOICES = (('Male', 'Male'),('Female', 'Female'),('other','others'))

    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    firstname = models.CharField(max_length=30,null=True, blank=True,validators =[validate_string], verbose_name='FirstName')
    lastname = models.CharField(max_length=30,null=True, blank=True,validators =[validate_string], verbose_name='LastName')
    dob = models.DateField(auto_now=False,null=True, blank=True, auto_now_add=False,validators =[validate_dob], verbose_name='Date of Birth')
    gender = models.CharField(max_length=7,null=True, blank=True, choices=GENDER_CHOICES, verbose_name='Gender')
    mobile = models.CharField(max_length=10,null=True, blank=True, validators =[validate_mobile], verbose_name='Mobile number')
    country = models.CharField(max_length=20,default="INDIA",choices=COUNTRY_CHOICES, verbose_name='Country')
    image = models.ImageField(null=True, blank=True,default='guprofileDB/default.png', upload_to='guprofileDB/')
    language = models.CharField(max_length=20, null=True, blank=True)
    guOTP = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username