from InnotterDjango.aws_metaclass import AWSMeta
from django.conf import settings


class SESClient(metaclass=AWSMeta):
    """
    SESClient: class which represents access to SES service with extra
    functionality to maintain innotter.
    """
    service_name = 'ses'

    @classmethod
    def send_email_about_new_post(cls, page_name: str, emails: list, posts_url: str) -> None:
        """
        send_email_about_new_post: sends notification to subscriber's email
        about new post.
            1) page_name - name of page where was created a new post;
            2) emails - list of subscribers' emails;
            3) posts_url - url to posts of the page.
        """
        cls.client.send_email(
            Source=settings.AWS_MAIL_SENDER,
            Destination={
                'ToAddresses': emails,
                'BccAddresses': emails
            },
            Message={
                'Subject': {
                    'Data': 'New post!',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': (
                            f'Hello! New post on the page {page_name}!<br>'
                            f'Link to the posts: <b><a href="{posts_url}">'
                            f'Posts on the page {page_name}</a></b>'
                        ),
                        'Charset': 'UTF-8'
                    }
                }
            }
        )

    @classmethod
    def send_email_to_verify_account(cls, email: str, verify_url: str) -> None:
        """
        send_email_to_verify_account: sends email to verify user registration.
            1) email - email which user specify when registering.
            2) verify_url - url which verify user's account.
        """
        cls.client.send_email(
            Source=settings.AWS_MAIL_SENDER,
            Destination={
                'ToAddresses': [email],
                'BccAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': 'Verify account!',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': (
                            f'Click the link below to verify account.<br>'
                            f'<b><a href="{verify_url}">{verify_url}</a></b>'
                        ),
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
