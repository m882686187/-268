# backend/accounts/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer

User = get_user_model()  # 获取当前用户模型

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful!"})
        return Response({"message": "Invalid credentials!"}, status=400)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # 需要用户认证
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # 获取当前登录用户
