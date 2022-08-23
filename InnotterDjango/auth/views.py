from auth.services import (
    create_response, set_tokens_to_cookie, get_payload_by_token
)
from auth.serializers import (
    SignUpSerializer, SignInSerializer
)
from rest_framework.decorators import action
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import status
from user.models import User
import jwt


class AuthViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'], serializer_class=SignUpSerializer)
    def sign_up(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=SignInSerializer)
    def sign_in(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = create_response(serializer.data, status=status.HTTP_200_OK)
        set_tokens_to_cookie(response, serializer.validated_data['id'])
        return response

    @action(detail=False, methods=['get'])
    def refresh(self, request):
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
