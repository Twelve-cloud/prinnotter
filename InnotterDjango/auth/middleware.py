from auth.services import create_response, get_payload_by_token
from rest_framework import status
from django.conf import settings
from user.models import User
import jwt


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        print(request.path)
        print(settings.NON_TOKEN_PATH)
        access_token = request.COOKIES.get('access_token', None)

        if access_token and request.path not in settings.NON_TOKEN_PATH:
            try:
                payload = get_payload_by_token(access_token)
                request.user = User.objects.get(pk=payload.get('id'))

                if request.user.is_blocked:
                    return create_response(
                        data={"Error": "User is blocked"},
                        status=status.HTTP_403_FORBIDDEN
                    )

            except User.DoesNotExist:
                return create_response(
                    data={'Error': 'User is not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            except jwt.ExpiredSignatureError:
                return create_response(
                    data={'Error': 'Unauthorized'},
                    status=status.HTTP_401_UNAUTHORIZED,
                    hdrs={'WWW-Authenticate': 'Refresh token'}
                )

        response = self.next(request)
        return response
