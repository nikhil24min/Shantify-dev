from django.contrib import admin
from .models import category, musictrack, playlist, playlist_song, music_reviews
# Register your models here.
admin.site.register(category)
admin.site.register(musictrack)
admin.site.register(playlist)
admin.site.register(playlist_song)
admin.site.register(music_reviews)
