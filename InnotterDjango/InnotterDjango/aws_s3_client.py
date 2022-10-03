from django.core.files.uploadedfile import InMemoryUploadedFile
from InnotterDjango.aws_metaclass import AWSMeta
from InnotterDjango.exceptions import BucketDoesNotExist
from botocore.exceptions import ClientError
from django.conf import settings
import io


class S3Client(metaclass=AWSMeta):
    """
    S3Client: class which represents access to S3 Bucket with extra
    functionality to maintain innotter.
    """
    service_name = 's3'

    @classmethod
    def upload_file(cls, image: InMemoryUploadedFile, key: str) -> None:
        """
        upload_file: uploads image to AWS S3 Bucket.
            1) image - object of InMemoryUploadedFile;
            2) key - full path to image in S3 Bucket.
        """
        try:
            bfile = io.BytesIO(image.read())
            cls.client.upload_fileobj(bfile, settings.AWS_BUCKET_NAME, key)
        except ClientError:
            raise BucketDoesNotExist()

    @classmethod
    def create_url(cls, key: str, expiration: int = 3600) -> str:
        """
        create_url: create url for image in AWS S3 Bucket.
            1) key - full path to image in S3 Bucket;
            2) expiration - lifetime of url in secs.
        """
        try:
            url = cls.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_BUCKET_NAME, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except ClientError:
            return BucketDoesNotExist()
