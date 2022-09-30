from user.services import (
    set_blocking, search_users_by_params, block_all_users_pages
)
from blog.models import Page
import pytest


pytestmark = pytest.mark.django_db


class TestUserServices:
    def test_set_blocking(self, user):
        assert user.is_blocked is False
        set_blocking(user=user, is_blocked=True)
        assert user.is_blocked is True

    def test_block_all_users_pages(self, page):
        block_all_users_pages(page.owner, is_blocked=True)
        page = Page.objects.get(pk=page.pk)
        assert page.unblock_date is not None

        block_all_users_pages(page.owner, is_blocked=False)
        page = Page.objects.get(pk=page.pk)
        assert page.unblock_date is None

    def test_search_users_by_params(self, user):
        users = search_users_by_params(username=user.username)
        assert user in users
