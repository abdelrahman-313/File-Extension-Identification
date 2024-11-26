# file_service/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Serve index.html at the root URL of the app
]
