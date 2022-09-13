from user.services import set_blocking
import pytest


pytestmark = pytest.mark.django_db


class TestUserServices:
    def test_set_blocking(self, user):
        assert user.is_blocked is False
        set_blocking(user=user, is_blocked=True)
        assert user.is_blocked is True
