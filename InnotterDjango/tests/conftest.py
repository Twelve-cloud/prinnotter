from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from model_bakery import baker
from user.models import User
import pytest


@pytest.fixture()
def api_factory():
    return APIRequestFactory()


@pytest.fixture()
def _request(mocker):
    return mocker.MagicMock()


@pytest.fixture()
def anon():
    return AnonymousUser()


@pytest.fixture()
def user():
    return baker.make(User, role='u')


@pytest.fixture()
def moder():
    return baker.make(User, role='m')


@pytest.fixture()
def admin():
    return baker.make(User, role='a')
