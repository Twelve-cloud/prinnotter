from InnotterDjango.aws_ses_client import SESClient
from InnotterDjango.celery import app
from user.models import User


@app.task
def send_notification_about_new_post(page_name: str, emails: list, posts_url: str) -> None:
    SESClient.send_email_about_new_post(page_name, emails, posts_url)


@app.task
def send_email_to_verify_account(email: str, verify_url: str) -> None:
    SESClient.send_email_to_verify_account(email, verify_url)


@app.task
def clear_database_from_waste_accounts() -> None:
    User.objects.filter(is_verified=False).delete()
