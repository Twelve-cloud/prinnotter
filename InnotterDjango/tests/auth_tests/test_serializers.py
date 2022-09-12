from jwt_auth.serializers import SignInSerializer
from rest_framework.serializers import ValidationError
import pytest


pytestmark = pytest.mark.django_db


class TestAuthSerializer:
    def test_validate(self, blocked_user, non_blocked_user):
        with pytest.raises(ValidationError):
            SignInSerializer.validate(..., {'email': None, 'password': ''})

        with pytest.raises(ValidationError):
            SignInSerializer.validate(..., {'email': '', 'password': None})

        with pytest.raises(ValidationError):
            SignInSerializer.validate(..., {'email': '', 'password': ''})

        with pytest.raises(ValidationError):
            serializer = SignInSerializer(data=blocked_user)
            serializer.is_valid(raise_exception=True)

        serializer = SignInSerializer(data=non_blocked_user)
        assert serializer.is_valid() is True
