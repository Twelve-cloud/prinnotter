import pytest


pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_user_view(self, user):
        assert user.__str__() == f'{user.id}: {user.username}'

    def test_user_get_absolute_url(self, user):
        assert user.get_absolute_url() == f'/users/{user.pk}/'
