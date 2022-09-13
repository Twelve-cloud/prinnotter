from model_bakery import baker
from user.models import User
import pytest


@pytest.fixture()
def user():
    return baker.make(User, role='u')


@pytest.fixture()
def moderator():
    return baker.make(User, role='m')


@pytest.fixture()
def admin():
    return baker.make(User, role='a')


@pytest.fixture()
def user_json():
    user = baker.prepare(User, role='u')
    return {
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'role': user.role
    }


@pytest.fixture()
def admin_json():
    admin = baker.prepare(User, role='a')
    return {
        'email': admin.email,
        'username': admin.username,
        'password': admin.password,
        'role': admin.role
    }


@pytest.fixture()
def update_json():
    return {
        'first_name': 'James',
        'last_name': 'Bond'
    }


@pytest.fixture()
def block_json():
    return {
        'is_blocked': 'True'
    }


@pytest.fixture()
def request_(mocker):
    return mocker.MagicMock()
