from django.urls import path, include
from . import views
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('test', views.getData, name='api_test'),
    path('orders', views.Orders.as_view(), name='api_test_post'),
    path('user/register',   CreateUserView.as_view(), name='register'),
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth', include("rest_framework.urls")),

] 