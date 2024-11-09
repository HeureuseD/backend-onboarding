from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 요청 데이터의 role 값이 STAFF라면 is_staff를 True로 설정.
            if request.data.get("role") == "STAFF":
                user.is_staff = True
                user.save()

            response_data = {
                "username": user.username,
                "nickname": user.nickname,
                "roles": serializer.get_roles(user)  # 역할을 포함한 응답 생성
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

