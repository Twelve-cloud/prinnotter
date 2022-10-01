from InnotterDjango.aws_ses_client import SESClient
import pytest


pytestmark = pytest.mark.django_db


class TestSESClient:
    def test_send_email_about_new_posts(self, mocker):
        send_email = mocker.MagicMock()
        mocker.patch.object(SESClient.client, 'send_email', send_email)
        SESClient.send_email_about_new_post(..., ..., ...)
        send_email.assert_called_once()

    def test_send_email_to_verify_account(self, mocker):
        send_email = mocker.MagicMock()
        mocker.patch.object(SESClient.client, 'send_email', send_email)
        SESClient.send_email_to_verify_account(..., ...)
        send_email.assert_called_once()
