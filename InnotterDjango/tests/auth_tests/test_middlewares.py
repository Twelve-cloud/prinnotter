from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jwt_auth.middleware import JWTMiddleware
import pytest


pytestmark = pytest.mark.django_db


class TestMiddleware:
    def test_call(self, _request, access_token, access_token_of_blocked_user, mocker):
        middleware = JWTMiddleware(mocker.MagicMock(return_value=None))

        with pytest.raises(AuthenticationFailed):
            middleware(_request)

        _request.COOKIES = {'access_token': access_token_of_blocked_user}
        with pytest.raises(PermissionDenied):
            middleware(_request)

        _request.COOKIES = {'access_token': access_token}
        assert middleware(_request) is None
