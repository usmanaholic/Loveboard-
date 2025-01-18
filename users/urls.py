from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.user_settings, name='settings'),
]