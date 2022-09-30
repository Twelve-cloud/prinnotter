from jwt_auth.services import generate_token
from django.conf import settings
from model_bakery import baker
from user.models import User
import pytest


@pytest.fixture(scope='session', autouse=True)
def secret_key():
    settings.SECRET_KEY = 'SECRET_KEY'


@pytest.fixture()
def access_data():
    user_id = 99
    access_token = generate_token(type='access', user_id=user_id)
    return access_token, user_id


@pytest.fixture()
def refresh_data():
    user_id = 100
    refresh_token = generate_token(type='refresh', user_id=user_id)
    return refresh_token, user_id


@pytest.fixture()
def blocked_user_json():
    user = baker.prepare(User, role='u', is_blocked=True)
    user.set_password('12341234')
    user.save()
    return {
        'email': user.email,
        'password': '12341234'
    }


@pytest.fixture()
def user_json():
    user = baker.prepare(User, role='u', is_verified=True)
    user.set_password('12341234')
    user.save()
    return {
        'email': user.email,
        'password': '12341234',
        'is_verified': user.is_verified
    }


@pytest.fixture()
def refresh_token(user):
    return generate_token(type='refresh', user_id=user.id)


@pytest.fixture()
def access_token(user):
    return generate_token(type='access', user_id=user.id)


@pytest.fixture()
def access_token_of_blocked_user():
    user = baker.make(User, role='u', is_blocked=True)
    return generate_token(type='access', user_id=user.id)
