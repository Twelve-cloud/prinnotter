from jwt_auth.services import (
    generate_token, set_tokens_to_cookie, get_payload_by_token
)
from rest_framework.response import Response
import pytest


pytestmark = pytest.mark.django_db


class TestAuthServices:
    def test_generate_token(self):
        with pytest.raises(ValueError):
            generate_token(type='random', user_id=993)

    def test_set_tokens_to_cookie(self):
        response = Response()
        set_tokens_to_cookie(response=response, user_id=993)

        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies

    def test_get_payload_by_token(self, access_data, refresh_data):
        access_token, access_user_id = access_data
        refresh_token, refresh_user_id = refresh_data

        access_payload = get_payload_by_token(access_token)
        refresh_payload = get_payload_by_token(refresh_token)

        assert access_payload['sub'] == access_user_id
        assert refresh_payload['sub'] == refresh_user_id
        assert get_payload_by_token('failed_token') is None
