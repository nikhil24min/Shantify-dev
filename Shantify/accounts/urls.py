from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.gulogin, name='gulogin'),
    path('logout/', views.gulogout, name='gulogout'),
    path('register/', views.guregister, name='guregister'),
    path('profile/', views.guprofile, name='guprofile'),
    path('profileupdate/', views.guprofileupdate, name='guprofileupdate'),

    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/pwd_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/pwd_reset__confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/pwd_reset__complete.html'), name='password_reset_complete'),      
]
