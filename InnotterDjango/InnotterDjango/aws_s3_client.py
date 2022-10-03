from InnotterDjango.aws_metaclass import AWSMeta
from django.conf import settings


class S3Client(metaclass=AWSMeta):
    service_name = 's3'

    @classmethod
    def upload_file(cls, file_name: str, object_name: str) -> None:
        response = cls.client.upload_file(file_name, settings.AWS_BUCKET_NAME, object_name)

        if not response:
            raise Exception(f'file "{file_name}" has been not uploaded')
