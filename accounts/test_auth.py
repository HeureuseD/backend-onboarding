import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    # 생성된 APIClient 객체를 반환
    return APIClient()

@pytest.mark.django_db
def test_signup_user_with_roles(api_client):
    # 회원가입 API 테스트
    url = reverse("signup")

    data = {
        "username": "JIN HO",
        "password": "12341234",
        "nickname": "Mentos",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED # API 호출이 성공적으로 수행되었는지 테스트
    assert response.data["username"] == data["username"] # 응답 데이터에 username이 맞게 포함되어 있는지 테스트
    assert response.data["nickname"] == data["nickname"] # 응답 데이터에 nickname이 맞게 포함되어 있는지 테스트
    assert "roles" in response.data # 응답 데이터에 roles가 포함되어 있는지 테스트
    assert response.data["roles"] == [{"role": "USER"}] # roles에 role이 맞게 포함됐는지 테스트
    user = User.objects.get(username="JIN HO")
    assert user.is_staff is False 

@pytest.mark.django_db
def test_login(api_client):
    # 로그인 API 테스트
    login_data = {
        "username": "JIN HO",
        "password": "12341234"
    }

    user = User.objects.create_user(username=login_data["username"], password=login_data["password"])

    url = reverse("token_obtain_pair")
    data = {
        "username": user.username,
        "password": login_data["password"]
    }

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK # 로그인 API 호출이 성공적으로 수행되었는지 확인
    assert "access" in response.data # 응답 데이터에 액세스 토큰이 포함되어 있는지 확인
    assert "refresh" in response.data # 응답 데이터에 리프레시 토큰이 포함되어 있는지 확인

@pytest.mark.django_db
def test_token_refresh(api_client):
    # 토큰 리프레시 API 테스트
    user = User.objects.create_user(username="testuser", password="testpassword123") # 사용자 객체 생성
    refresh = RefreshToken.for_user(user)
    url = reverse("token_refresh")
    data = {
        "refresh": str(refresh)
    }

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK # 토큰 갱신 API 호출이 성공적으로 수행되었는지 확인
    assert "access" in response.data # 응답 데이터에 새로운 액세스 토큰이 포함되어 있는지 확인

@pytest.mark.django_db
def test_logout(api_client):
    # 로그아웃 API 테스트
    user = User.objects.create_user(username="testuser", password="testpassword123") # 사용자 객체 생성
    refresh = RefreshToken.for_user(user)
    url = reverse("logout")
    data = {
        "refresh": str(refresh)
    }

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_205_RESET_CONTENT # 로그아웃이 성공적으로 수행되었는지 테스트
