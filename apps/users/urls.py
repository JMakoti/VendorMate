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
    path('editprofile/', AddprofileDetails, name='edit_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('change_credentials/', change_user_credentials, name='change_user_credentials'),
    # path('manage_user/<int:user_id>/', manage_user_details, name='manage_user_details'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
