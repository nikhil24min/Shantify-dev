from django.urls import path

from . import views

urlpatterns = [
    path('', views.musiclist, name='musiclist'),
    path('musicinfo/<str:pk>', views.music_info, name='music_info'),
    path('musiclike/', views.music_like, name='music_like'),

    path('musicreviews/<int:pk>', views.reviews_list, name='reviews_list'),
    path('delreview/<int:pk>', views.delreview, name='del_review'),
    path('editreview/<int:pk>', views.editreview, name='edit_review'),

    path('playlist/', views.playlist_list, name='playlist'),
    path('playlistplayer/<int:pk>', views.playlistplayer, name='playlistplayer'),
    path('musicplayer/', views.musicplayer, name='musicplayer'),

    path('questions/', views.questions, name='questions'),
    # path('search/', views.music_search_list, name='music_search'),
    # path('onesongplayer/<int:pk>', views.onesongplayer, name='onesongplayer'),
]