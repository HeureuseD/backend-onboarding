from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupAPIView, LogoutAPIView, CustomTokenObtainPairView

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("signin/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]