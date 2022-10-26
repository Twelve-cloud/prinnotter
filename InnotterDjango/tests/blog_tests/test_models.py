import pytest


pytestmark = pytest.mark.django_db


class TestTagModel:
    def test_tag_view(self, tag):
        assert tag.__str__() == f'{tag.id}. {tag.name}'

    def test_tag_get_absolute_url(self, tag):
        assert tag.get_absolute_url() == f'/tags/{tag.pk}/'


class TestPageModel:
    def test_page_view(self, page):
        assert page.__str__() == f'{page.id}. {page.name}'

    def test_page_get_absolute_url(self, page):
        assert page.get_absolute_url() == f'/pages/{page.pk}/'


class TestPostModel:
    def test_post_view(self, post):
        assert post.__str__() == f'id: {post.pk}, page: {post.page.name}'

    def test_post_get_absolute_url(self, post):
        assert post.get_absolute_url() == f'/posts/{post.pk}/'
