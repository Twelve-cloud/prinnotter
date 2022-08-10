from django.conf import settings
from rest_framework import status
from user.services import create_response
from user.models import User
import jwt


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token', None)

        if access_token and request.path not in settings.NON_TOKEN_PATH:
            try:
                payload = jwt.decode(
                    access_token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                request.user = User.objects.get(pk=payload.get('id'))

                if request.user.is_blocked:
                    return create_response(
                        data={"Error": "User is blocked"},
                        status=status.HTTP_403_FORBIDDEN
                    )

            except User.DoesNotExist:
                return create_response(
                    data={"Error": "User is not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            except jwt.ExpiredSignatureError:
                response = create_response(
                    data={"Error": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                response.headers['WWW-Authenticate'] = 'Refresh Token'
                return response

        response = self.next(request)

        return response
