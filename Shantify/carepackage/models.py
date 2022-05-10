from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import datetime
import re

from musicplayer.models import musictrack

def validate_string(value):
    if re.match(r'^[A-Z a-z]*$', value):
        return True
    else:
        raise ValidationError('Only Alphabets are allowed')

def validate_dob(value):
    dob = value
    age = (datetime.date.today() - dob).days/365
    if age < 18:
        raise ValidationError('Must be at least 18 years old to register')
    return value

def validate_mobile(value):
    if not value.isdigit():
        raise ValidationError('Mobile number should be a number')

    if len(str(value)) == 10:
        return value
    else:
        raise ValidationError('Mobile number should be 10 digits long.')

class therapist(models.Model):
    GENDER_CHOICES = (('Male', 'Male'),('Female', 'Female'),('other','others'))

    tfirstname = models.CharField(max_length=30,null=True, blank=True,validators =[validate_string], verbose_name='FirstName')
    tlastname = models.CharField(max_length=30,null=True, blank=True,validators =[validate_string], verbose_name='LastName')
    tdob = models.DateField(auto_now=False,null=True, blank=True, auto_now_add=False,validators =[validate_dob], verbose_name='Date of Birth')
    tgender = models.CharField(max_length=7,null=True, blank=True, choices=GENDER_CHOICES, verbose_name='Gender')
    tmobile = models.CharField(max_length=10,null=True, blank=True, validators =[validate_mobile], verbose_name='Mobile number')
    temail = models.EmailField(blank=True, null=True)
    tcountry = models.CharField(max_length=20,default="INDIA", verbose_name='Country')
    timage = models.ImageField(null=True, blank=True,default='therapistDB/default.png', upload_to='therapistDB/')
    tlicense = models.CharField(max_length=20,default="0001", verbose_name='Licence number')

    def __str__(self):
        return self.tfirstname

class carepack(models.Model):
    pack_name = models.CharField(max_length=30,null=True, blank=True,validators =[validate_string], verbose_name='Pack name')
    pack_desc = models.TextField(max_length=500, null=True, blank=True, verbose_name="Pack Description")
    pack_image = models.ImageField(null=True, blank=True,default='packcoverDB/default.png', upload_to='packcoverDB/')
    subscribed_count = models.IntegerField(blank=True, null=True, default=0)

    pack_pdf = models.FileField(null=True, blank=True,default='packpdfDB/default.png', upload_to='packpdfDB/')
    pack_tracks = models.ManyToManyField(musictrack, related_name="packtracks", default=None, blank=True)

    uploaded_date = models.DateField(verbose_name='Uploaded date', auto_now_add=True )
    uploaded_by = models.ForeignKey(User, verbose_name="Uploaded By", default = 1, on_delete=models.SET_DEFAULT)

    prepared_by = models.ForeignKey(therapist, verbose_name="Therapist", default = 1, on_delete=models.SET_DEFAULT)
    
    def __str__(self):
        return self.pack_name


class packsubscribe(models.Model):
    suser = models.ForeignKey(User, verbose_name="User", blank=True, on_delete=models.CASCADE)
    pack_subscribed = models.ForeignKey(carepack, verbose_name="Pack subscribed",  on_delete=models.CASCADE)

    subscribed_date = models.DateField(verbose_name='Subscribed date', auto_now_add=True )
    completed = models.BooleanField(verbose_name='Pack completed', default=False)

    def __str__(self):
        return self.suser.username+" - "+self.pack_subscribed.pack_name