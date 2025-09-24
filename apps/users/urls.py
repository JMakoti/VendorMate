from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from  .views import *

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('users/', get_all_users, name='get_all_users'),
    path('change_credentials/', change_user_credentials, name='change_user_credentials'),
]
