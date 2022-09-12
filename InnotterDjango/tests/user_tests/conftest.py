import pytest
from user.models import User
from model_bakery import baker


@pytest.fixture()
def created_user():
    return baker.make(User, role='u')


@pytest.fixture()
def created_moderator():
    return baker.make(User, role='m')


@pytest.fixture()
def created_admin():
    return baker.make(User, role='a')


@pytest.fixture()
def prepared_user():
    return baker.prepare(User, role='u')


@pytest.fixture()
def prepared_moderator():
    return baker.prepare(User, role='m')


@pytest.fixture()
def prepared_admin():
    return baker.prepare(User, role='a')


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
def moderator_json():
    moderator = baker.prepare(User, role='m')
    return {
        'email': moderator.email,
        'username': moderator.username,
        'password': moderator.password,
        'role': moderator.role
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
