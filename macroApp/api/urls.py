from django.urls import path, include
from . import views
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('profile', views.Profile_Create.as_view(), name ='create_profile'),
    path('profile/delete/<int:pk>', views.Profile_Delete.as_view(), name = 'delete_profile'),
    path('favorite', views.Favorite_Create.as_view(), name ='add_fav'),
    path('favorite/delete/<int:pk>', views.Favorite_Delete.as_view(), name = 'delete_fav'),
    path('test', views.getData, name='api_test'),
    path('orders', views.Orders.as_view(), name='api_test_post'),
    path('user/register',   CreateUserView.as_view(), name='register'),
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth', include("rest_framework.urls")),


] 