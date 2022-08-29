from jwt_auth.services import set_tokens_to_cookie, get_payload_by_token
from jwt_auth.serializers import SignInSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status


class AuthViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'], serializer_class=SignInSerializer)
    def sign_in(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        set_tokens_to_cookie(response, serializer.validated_data['id'])
        return response

    @action(detail=False, methods=['get'])
    def refresh(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)
        payload = get_payload_by_token(refresh_token)

        if payload is None:
            return Response(
                data={'Refresh Token': 'Expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user = User.objects.get(pk=payload.get('sub'))

        response = Response(
            data={'Tokens': 'OK'},
            status=status.HTTP_200_OK
        )
        set_tokens_to_cookie(response, request.user.id)

        return response
        # If front-end will get 400_BAD_REQUEST
        # It will remove refresh token from cookie
        # and request to /auth/jwt/sign_in
        # without any tokens in a cookie
