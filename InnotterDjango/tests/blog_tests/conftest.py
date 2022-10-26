from blog.views import PageViewSet, PostViewSet
from blog.models import Tag, Post
from model_bakery import baker
import pytest


@pytest.fixture()
def tag():
    return baker.make(Tag)


@pytest.fixture()
def post(page):
    return baker.make(Post, page=page)


@pytest.fixture()
def block_json():
    return {
        'unblock_date': '2025-09-26 00:00:00'
    }


@pytest.fixture()
def user_json(user):
    return {
        'user_id': user.id
    }


@pytest.fixture()
def post_json(page):
    post = baker.prepare(Post, page=page)
    return {
        'page': post.page.id,
        'content': post.content
    }


@pytest.fixture()
def pageperm(mocker):
    mock = mocker.MagicMock(return_value=True)
    mocker.patch.object(PageViewSet, 'check_permissions', mock)
    mocker.patch.object(PageViewSet, 'check_object_permissions', mock)


@pytest.fixture()
def postperm(mocker):
    mock = mocker.MagicMock(return_value=True)
    mocker.patch.object(PostViewSet, 'check_permissions', mock)
    mocker.patch.object(PostViewSet, 'check_object_permissions', mock)
