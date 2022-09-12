from user.services import set_blocking
import pytest


pytestmark = pytest.mark.django_db


class TestUserServices:
    def test_set_blocking(self, created_user):
        assert created_user.is_blocked is False
        set_blocking(user=created_user, is_blocked=True)
        assert created_user.is_blocked is True
