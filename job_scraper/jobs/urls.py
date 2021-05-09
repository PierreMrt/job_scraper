from . import views
from django.urls import path

urlpatterns = [
    path('', views.forms, name='home')
]