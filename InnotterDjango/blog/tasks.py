from InnotterDjango.aws_clients import SESClient
from InnotterDjango.celery import app


@app.task
def send_notification_about_new_post(page_name, emails, posts_url):
    SESClient.send_email_about_new_post(page_name, emails, posts_url)


@app.task
def send_email_to_verify_account(email, verify_url):
    SESClient.send_email_to_verify_account(email, verify_url)
