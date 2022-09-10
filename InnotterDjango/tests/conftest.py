from rest_framework.test import APIRequestFactory
import pytest

@pytest.fixture()
def api_factory():
    return APIRequestFactory()
