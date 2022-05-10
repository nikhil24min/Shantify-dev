from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import datetime
import re

from mutagen.mp3 import MP3
import os

def validate_string(value):
    if re.match(r'^[A-Z a-z]*$', value):
        return True
    else:
        raise ValidationError('Only Alphabets are allowed')

def validate_is_audio(file):

    print(file)
    # try:
    #     audio = MP3(file)

    #     if not audio :
    #         raise TypeError()

    #     first_file_check=True
        
    # except Exception as e:
    #     first_file_check=False
    
    # if not first_file_check:
    #     raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.mp3']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')

# Category model --- categories of mental states
class category(models.Model):
    category_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="category name",validators =[validate_string])
    category_desc = models.TextField(max_length=100, null=True, blank=True, verbose_name="Description")
    cat_score = models.IntegerField(null=True, blank=True, default=0, verbose_name="Score")

    def __str__(self):
        return self.category_name



# Music tracks --- actual music info and files

# getting audi length
def get_audio_length(file):
    audio = MP3(file)
    return audio.info.length


class musictrack(models.Model):
    track_name = models.CharField(verbose_name="Track name", max_length=30, null=False, blank=False,validators =[validate_string])
    track_path = models.FileField(verbose_name="Track path", upload_to='musicDB/',validators=[validate_is_audio])
    duration = models.DecimalField(max_digits=20, decimal_places=2,verbose_name="Track duration", default=0,blank = True)
    cover_image = models.ImageField(verbose_name="Track image", default = 'musiccoverDB/defaultcover.jpg',upload_to='musiccoverDB/')
    track_creator = models.CharField(verbose_name="Track creator", default="Ananymous",max_length=30, null=False, blank=False,validators =[validate_string])

    uploaded_date = models.DateField(verbose_name='Uploaded date', auto_now_add=True )
    uploaded_by = models.ForeignKey(User, verbose_name="Uploaded By", default = 1, on_delete=models.SET_DEFAULT)
    #category_id = models.ForeignKey(category, verbose_name="category", default = 1, on_delete=models.SET_DEFAULT)
    likes_count = models.IntegerField(verbose_name="Likes count",default = 0, blank=True)
    likes = models.ManyToManyField(User, related_name="like", default=None, blank=True)
    reviews_count = models.IntegerField(verbose_name="Reviews count",default = 0, blank=True)

    def save(self,*args, **kwargs):
        if not self.duration:
            # logic for getting length of audio
            duration=get_audio_length(self.track_path)
            self.duration =f'{duration:.2f}'

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.track_name

# playlist ---- playlist 
class playlist(models.Model):
    playlist_name = models.CharField(verbose_name="Playlist name", max_length=30, null=False, blank=False,validators =[validate_string])
    uploaded_date = models.DateField(verbose_name='Uploaded date', auto_now_add=True )
    uploaded_by = models.ForeignKey(User, verbose_name="Uploaded By", default = 1, on_delete=models.SET_DEFAULT)
    category_fk = models.ForeignKey(category, verbose_name="Category", default = 1, on_delete=models.CASCADE)
    musictracks = models.ManyToManyField(musictrack, related_name="musictracks", default=None, blank=True)
    cover_image = models.ImageField(verbose_name="Playlist cover", default = 'musiccoverDB/defaultcover.jpg',upload_to='musiccoverDB/')
    def __str__(self):
        return self.playlist_name

# playlist - song  ---- mapping song to playlist
class playlist_song(models.Model):
    playlist_fk = models.ForeignKey(playlist, verbose_name="playlist name",  on_delete=models.CASCADE)
    track_fk = models.ForeignKey(musictrack, verbose_name="track name",  on_delete=models.CASCADE)

# music review ---- music review given by users
class music_reviews(models.Model):
    review_text = models.TextField(verbose_name="Review", max_length=200)
    reviewed_by = models.ForeignKey(User, blank=True,verbose_name="Reviewed By", on_delete=models.CASCADE)
    track_fk = models.ForeignKey(musictrack, blank=True, verbose_name="track name",  on_delete=models.CASCADE)
    reviewed_date = models.DateField(verbose_name='Review date', auto_now_add=True )

    def __str__(self):
        return self.reviewed_by.username


class questionnaire(models.Model):
    question = models.TextField(verbose_name="Question", max_length=200)
    score = models.IntegerField(verbose_name="score for true",default = 1, blank=True)
    
    def __str__(self):
        return self.reviewed_date





# redundant model......dont use this
class music_review(models.Model):
    review = models.TextField(verbose_name='Review', max_length=600)
    review_track = models.ForeignKey(musictrack, verbose_name="Reviewd track", default=1, on_delete=models.CASCADE)
    reviewed_date = models.DateField(verbose_name='Reviewed date', auto_now_add=True )
    reviewed_by = models.ForeignKey(User, verbose_name="Reviewed By", default = 1, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.reviewed_by.user

