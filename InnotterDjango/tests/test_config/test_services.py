from InnotterDjango.services import (
    add_image_to_s3_bucket, validate_image, add_url_to_request
)
from InnotterDjango.exceptions import InvalidImageExtenstion
from InnotterDjango.aws_s3_client import S3Client
from django.http import QueryDict
import pytest

pytestmark = pytest.mark.django_db


class TestConfigServices:
    def test_add_image_to_s3_bucker(self, mocker):
        image = mocker.MagicMock()
        image.name = mocker.MagicMock()
        upload_file = mocker.MagicMock()
        mocker.patch.object(S3Client, 'upload_file', upload_file)

        validate_img = mocker.MagicMock(return_value=True)
        mocker.patch('InnotterDjango.services.validate_image', validate_img)
        add_image_to_s3_bucket(image, '')
        upload_file.assert_called_once()
        validate_img.assert_called_once()

        validate_img = mocker.MagicMock(return_value=False)
        mocker.patch('InnotterDjango.services.validate_image', validate_img)
        with pytest.raises(InvalidImageExtenstion):
            add_image_to_s3_bucket(image, '')

    def test_validate_image(self):
        image = 'image.jpg'
        assert validate_image(image) is True
        image = 'image.unk'
        assert validate_image(image) is False

    def test_add_url_to_requests(self, mocker):
        request = mocker.MagicMock()
        request.data = QueryDict()
        add_url_to_request(..., request)
        'image' in request.data
        request.data = {}
        add_url_to_request(..., request)
        'image' in request.data
