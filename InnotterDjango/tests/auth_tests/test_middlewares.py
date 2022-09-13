from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jwt_auth.middleware import JWTMiddleware
from rest_framework import status
import pytest


pytestmark = pytest.mark.django_db


class TestMiddleware:
    def test_call(self, access_token, access_token_of_blocked_user, mocker):
        middleware = JWTMiddleware(mocker.MagicMock(return_value=None))
        request = mocker.MagicMock()

        with pytest.raises(AuthenticationFailed):
            middleware(request)

        request.COOKIES = {'access_token': access_token_of_blocked_user}
        with pytest.raises(PermissionDenied):
            middleware(request)

        request.COOKIES = {'access_token': access_token}
        assert middleware(request) is None
