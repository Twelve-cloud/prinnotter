from jwt_auth.services import generate_token
import pytest


@pytest.fixture()
def access_data():
    user_id = 99
    access_token = generate_token(type='access', user_id=99)
    return access_token, user_id


@pytest.fixture()
def refresh_data():
    user_id = 100
    refresh_token = generate_token(type='refresh', user_id=user_id)
    return refresh_token, user_id
