from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

urlpatterns = [
    path("", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path("token/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("me/", views.UserAPIView.as_view(), name="user-info"),
]

app_name = "user"
