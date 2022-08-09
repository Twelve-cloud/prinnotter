from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.serializers import (
    UserSerializer, RegistrationSerializer, LoginSerializer
)
from django.conf import settings
from django.shortcuts import redirect
from user.models import User
from user.services import create_response
import jwt


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
            serializer.validated_data.get('access_token'),
            secure=True,
            httponly=True
        )

        response.set_cookie(
            'refresh_token',
            serializer.validated_data.get('refresh_token'),
            secure=True,
            httponly=True
        )

        return response


class RefreshTokenApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)

        if refresh_token:
            try:
                payload = jwt.decode(
                    refresh_token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                user = User.objects.get(pk=payload.get('id'))

                response = create_response(
                    data={"Tokens": 'OK'},
                    status=status.HTTP_200_OK
                )

                response.set_cookie(
                    'access_token',
                    user.generate_access_token(),
                    secure=True,
                    httponly=True
                )

                response.set_cookie(
                    'refresh_token',
                    user.generate_refresh_token(),
                    secure=True,
                    httponly=True
                )

                return response

            except User.DoesNotExist:
                return create_response(
                    data={"Error": "User is not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except jwt.ExpiredSignatureError:
                return redirect('login')


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
