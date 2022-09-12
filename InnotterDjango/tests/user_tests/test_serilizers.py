from user.serializers import UserSerializer
from django.db.utils import IntegrityError
from user.models import User
import pytest


pytestmark = pytest.mark.django_db


class TestUserSerializer:
    def test_create(self, user_json, admin_json):
        user = UserSerializer.create(..., user_json)
        assert user.email == user_json['email']
        assert user.role == user_json['role']
        assert user.pk is not None

        admin = UserSerializer.create(..., admin_json)
        assert admin.email == admin_json['email']
        assert admin.role == admin_json['role']
        assert admin.is_superuser is True
        assert admin.pk is not None

        with pytest.raises(IntegrityError):
            UserSerializer.create(..., user_json)

    def test_update(self, created_user, update_json):
        serializer = UserSerializer()
        user = serializer.update(created_user, update_json)

        assert user.first_name == update_json['first_name']
        assert user.last_name == update_json['last_name']
