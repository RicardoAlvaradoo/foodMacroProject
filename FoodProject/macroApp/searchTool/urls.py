from django.urls import path
from . import views

urlpatterns = [
    path('', views.searchTool, name='searchTool'),
]