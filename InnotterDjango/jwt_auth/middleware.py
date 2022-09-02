from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jwt_auth.services import get_payload_by_token
from user.services import get_user_by_id
from user.models import User


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token', None)

        if access_token and request.path != '/api/v1/auth/jwt/sign_in/' and request.path != '/api/v1/auth/jwt/refresh/' and request.path != '/api/v1/admin/' and request.path != '/api/v1/admin/login/':
            payload = get_payload_by_token(access_token)

            if payload is None:
                raise AuthenticationFailed(detail='Unauthorized')

            request.user = get_user_by_id(payload.get('sub'))

            if not request.user:
                raise AuthenticationFailed(detail='Unauthorized')

            if request.user.is_blocked:
                raise PermissionDenied(detail='User is blocked')
                # If front-end will get HTTP_401_UNAUTHORIZED
                # It'll delete access token from cookie and
                # set refresh token to a cookie and request to
                # /auth/jwt/refresh to get new tokens

        response = self.next(request)
        return response
