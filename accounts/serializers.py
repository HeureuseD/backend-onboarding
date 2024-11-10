from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'roles']
        extra_kwargs = {'password': {'write_only': True}} # 쓰기 전용 필드

    def get_roles(self, obj): 
        roles = [{"role": "USER"}] # 기본적으로 role은 USER로 설정됨. 
        if obj.is_staff: 
            roles.append({"role": "STAFF"})
        return roles

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data = {'token': data['access']}
        return data