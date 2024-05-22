from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.home),
   path('contact/', views.contact, name='contact'),
   path('support/', views.support, name='support'),
   path('privacy/', views.privacy, name='privacy'),
   path('terms/', views.terms, name='terms'),
]
