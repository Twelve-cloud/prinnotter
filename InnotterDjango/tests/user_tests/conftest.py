import pytest
from user.models import User
from model_bakery import baker


@pytest.fixture()
def created_user():
    return baker.make(User, role='u')


@pytest.fixture()
def prepared_user():
    return baker.prepare(User, role='u')
