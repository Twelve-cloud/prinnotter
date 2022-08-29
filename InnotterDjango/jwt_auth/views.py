from jwt_auth.services import set_tokens_to_cookie, get_new_tokens
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
        new_tokes = get_new_tokens(request, refresh_token)

        if new_tokes is None:
            return Response(
                data={'Refresh Token': 'Expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return new_tokes
