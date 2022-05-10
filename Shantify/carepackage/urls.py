from django.urls import path

from . import views

urlpatterns = [
    path('', views.packlist, name='packlist'),
    path('packinfo/<int:pk>/', views.packinfo, name='packinfo'),

    path('therapistlist/', views.therapistlist, name='therapistlist'),
    path('therapistinfo/<int:pk>/', views.therapistinfo, name='therapistinfo'),

    path('mysubs/', views.mysubs, name='mysubs'),
    path('packageplaylist/<int:pk>/', views.packageplaylist, name='packageplaylist'),
    
]