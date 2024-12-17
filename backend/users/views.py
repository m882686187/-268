from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers

# 用户序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # 可以根据需要添加其他字段

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"User: {user}, Is Authenticated: {user.is_authenticated}")

        # 如果用户已认证，返回用户信息
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
