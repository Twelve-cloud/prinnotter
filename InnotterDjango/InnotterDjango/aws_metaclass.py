from django.conf import settings
from typing import NewType
import boto3


class AWSMeta(type):
    """
    AWSMeta: metaclass, which must be added to all AWS clients classes.
    Automatically provides aws credentials for every AWS client class.
    """
    def __new__(meta, classname: str, supers: tuple, classdict: dict) -> NewType:
        """
        __new__: Automatically provides aws credentials for every
        AWS client class and checks if service_name in class or not
        after that creates class object.
        """
        if 'service_name' in classdict:
            classdict['client'] = boto3.client(
                classdict['service_name'],
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME if settings.AWS_REGION_NAME else 'us-west-2'
            )
        else:
            raise Exception('Fatal error: service_name must be specified!')
        return type.__new__(meta, classname, supers, classdict)
