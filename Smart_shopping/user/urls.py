from django.urls import path
from . import views

urlpatterns = [
    path('recent_history/', views.get_recent_history, name='get_recent_history'),
    path('saved_history/', views.get_saved_history, name='saved_history'),
    path('check_history/', views.check_history, name='check_history'),
    path('', views.profile, name='profile')
]