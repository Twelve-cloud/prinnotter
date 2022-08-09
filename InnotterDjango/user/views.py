from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.serializers import (
    UserSerializer, RegistrationSerializer, LoginSerializer
)
from user.models import User


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email', {}),
            'username': request.data.get('username', {}),
            'password': request.data.get('password', {}),
            'role': request.data.get('role', {})
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email', {}),
            'password': request.data.get('password', {}),
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        response.set_cookie(
            'access_token',
            serializer.validated_data.get('access_token')
        )

        response.set_cookie(
            'refresh_token',
            serializer.validated_data.get('refresh_token')
        )

        return response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
