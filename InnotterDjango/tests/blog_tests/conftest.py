from blog.models import Tag, Page, Post
from model_bakery import baker
from user.models import User
import pytest


@pytest.fixture()
def user():
    return baker.make(User, role='u')


@pytest.fixture()
def tag():
    return baker.make(Tag)


@pytest.fixture()
def page(user):
    return baker.make(Page, owner=user)


@pytest.fixture()
def post(page):
    return baker.make(Post, page=page)
