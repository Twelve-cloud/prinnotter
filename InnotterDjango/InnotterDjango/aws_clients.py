from django.conf import settings
import boto3


class AWSMeta(type):
    def __new__(meta, classname, supers, classdict):
        if 'service_name' in classdict:
            classdict['client'] = boto3.client(
                classdict['service_name'],
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME
            )
        else:
            raise 'Fatal error: service_name must be specified!'
        return type.__new__(meta, classname, supers, classdict)


class SESClient(metaclass=AWSMeta):
    service_name = 'ses'

    @classmethod
    def send_email_about_new_post(cls, page_name, emails, posts_url):
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
