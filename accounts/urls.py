from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView 
from .views import SignupAPIView, LogoutView

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
]