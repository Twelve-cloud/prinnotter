from user.services import (
    create_response, set_tokens_to_cookie, get_payload_by_token
)
from user.serializers import (
    UserSerializer, RegistrationSerializer, LoginSerializer
)
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import status
from user.models import User
import jwt


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = create_response(serializer.data, status=status.HTTP_200_OK)
        set_tokens_to_cookie(response, serializer.validated_data['id'])
        return response


class RefreshTokenApiView(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)

        if refresh_token:
            try:
                payload = get_payload_by_token(refresh_token)
                request.user = User.objects.get(pk=payload.get('id'))

                response = create_response(
                    data={'Tokens': 'OK'},
                    status=status.HTTP_200_OK
                )
                set_tokens_to_cookie(response, request.user.id)

                return response

            except User.DoesNotExist:
                return create_response(
                    data={'Error': 'User is not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            except jwt.ExpiredSignatureError:
                request.COOKIES.clear()
                return redirect('login')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
