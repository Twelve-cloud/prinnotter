from django.core.files.uploadedfile import InMemoryUploadedFile
from InnotterDjango.aws_metaclass import AWSMeta
from InnotterDjango.exceptions import BucketDoesNotExist
from botocore.exceptions import ClientError
from django.conf import settings
import io


class S3Client(metaclass=AWSMeta):
    service_name = 's3'

    @classmethod
    def upload_file(cls, image: InMemoryUploadedFile, key: str) -> None:
        try:
            bfile = io.BytesIO(image.read())
            cls.client.upload_fileobj(bfile, settings.AWS_BUCKET_NAME, key)
        except ClientError:
            raise BucketDoesNotExist()

    @classmethod
    def create_url(cls, key: str, expiration: int = 3600) -> str:
        try:
            url = cls.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_BUCKET_NAME, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except ClientError:
            return BucketDoesNotExist()
