from InnotterDjango.aws_s3_client import S3Client
from InnotterDjango.exceptions import InvalidImageExtenstion
from django.http import HttpRequest, QueryDict


def add_image_to_s3_bucket(image, folder):
    """
    add_image_to_s3_bucket: validate image, add it to s3 bucket if it's valid,
    if it's not valid raise an exception.
    """
    is_valid = validate_image(image.name)

    if is_valid:
        S3Client.upload_file(image, folder + '/' + image.name)
        pass
    else:
        raise InvalidImageExtenstion()


def validate_image(image_name: str):
    """
    validate_image: checks whether picture contains acceptable extensions.
    If it does then returns True, otherwise False.
    """
    acceptable_extensions = ['jpg', 'png']
    return True if image_name[-3:] in acceptable_extensions else False


def add_url_to_request(url: str, request: HttpRequest) -> None:
    """
    add_url_to_request: added url to request data.
    """
    if isinstance(request.data, QueryDict):
        request.data._mutable = True
        request.data['image'] = url
        request.data._mutable = False
        return
    request.data['image'] = url
