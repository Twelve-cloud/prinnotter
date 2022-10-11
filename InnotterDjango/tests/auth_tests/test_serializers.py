from rest_framework.serializers import ValidationError
from jwt_auth.serializers import SignInSerializer
import pytest


pytestmark = pytest.mark.django_db


class TestAuthSerializer:
    def test_validate(self, blocked_user_json, user_json):
        with pytest.raises(ValidationError):
            SignInSerializer.validate(..., {'email': None, 'password': ''})

        with pytest.raises(ValidationError):
            SignInSerializer.validate(..., {'email': '', 'password': None})

        with pytest.raises(ValidationError):
            SignInSerializer.validate(..., {'email': '', 'password': ''})

        with pytest.raises(ValidationError):
            serializer = SignInSerializer(data=blocked_user_json)
            serializer.is_valid(raise_exception=True)

        serializer = SignInSerializer(data=user_json)
        assert serializer.is_valid() is True
