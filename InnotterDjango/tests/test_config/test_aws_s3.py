from InnotterDjango.exceptions import BucketDoesNotExist
from InnotterDjango.aws_s3_client import S3Client
from botocore.exceptions import ClientError
import pytest

pytestmark = pytest.mark.django_db


class TestS3Client:
    def test_upload_file(self, mocker):
        image = mocker.MagicMock()
        image.read = mocker.MagicMock(return_value=b'')

        upload_file = mocker.MagicMock()
        mocker.patch.object(S3Client.client, 'upload_fileobj', upload_file)
        S3Client.upload_file(image, ...)
        upload_file.assert_called_once()

        upload_file = mocker.MagicMock(side_effect=ClientError({}, ''))
        mocker.patch.object(S3Client.client, 'upload_fileobj', upload_file)
        with pytest.raises(BucketDoesNotExist):
            S3Client.upload_file(image, ...)

    def test_create_url(self, mocker):
        create_url = mocker.MagicMock()
        mocker.patch.object(S3Client.client, 'generate_presigned_url', create_url)
        S3Client.create_url(..., ...)
        create_url.assert_called_once()

        create_url = mocker.MagicMock(side_effect=ClientError({}, ''))
        mocker.patch.object(S3Client.client, 'generate_presigned_url', create_url)
        with pytest.raises(BucketDoesNotExist):
            S3Client.create_url(..., ...)
