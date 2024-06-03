from django.urls import path
from .import views

urlpatterns = [
    path('test', views.getData, name='api_test'),
    path('orders', views.orders, name='api_test_post')

]