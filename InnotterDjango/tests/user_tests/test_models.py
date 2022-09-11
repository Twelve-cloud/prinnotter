from user.models import User
import pytest


pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_user_view(self, created_user):
        assert created_user.__str__() == f'{created_user.id}: {created_user.username}'

    def test_user_get_absolute_url(self, created_user):
        assert created_user.get_absolute_url() == f'/users/{created_user.pk}/'
