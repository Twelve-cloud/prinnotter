from InnotterDjango.tasks import (
    send_notification_about_new_post, send_email_to_verify_account,
    clear_database_from_waste_accounts
)
from InnotterDjango import aws_ses_client
from user.models import User
import pytest


pytestmark = pytest.mark.django_db


class TestTasks:
    def test_send_notification_about_new_posts(self, mocker):
        send_notif = mocker.MagicMock()
        mocker.patch.object(aws_ses_client.SESClient, 'send_email_about_new_post', send_notif)
        send_notification_about_new_post(..., ..., ...)
        send_notif.assert_called_once()

    def test_send_email_to_verify_account(self, mocker):
        send_email = mocker.MagicMock()
        mocker.patch.object(aws_ses_client.SESClient, 'send_email_to_verify_account', send_email)
        send_email_to_verify_account(..., ...)
        send_email.assert_called_once()

    def test_clear_database_from_waste_accounts(self, mocker, user):
        clear_database_from_waste_accounts()
        assert user not in User.objects.all()
