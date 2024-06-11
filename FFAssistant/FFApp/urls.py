# In myapp/urls.py, set up the URL for your view
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]