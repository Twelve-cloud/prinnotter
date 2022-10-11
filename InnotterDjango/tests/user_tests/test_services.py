from user.services import (
    set_blocking, block_all_users_pages, send_verification_link
)
from InnotterDjango.tasks import send_email_to_verify_account
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

    def test_send_verification_link(self, mocker):
        gen_token = mocker.MagicMock(return_value='')
        send_email = mocker.MagicMock()

        mocker.patch('user.services.generate_token', gen_token)
        mocker.patch.object(send_email_to_verify_account, 'delay', send_email)
        send_verification_link('', '')

        gen_token.assert_called_once()
        send_email.assert_called_once()
