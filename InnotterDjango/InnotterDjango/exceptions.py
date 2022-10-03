from rest_framework.exceptions import APIException


class InvalidImageExtenstion(APIException):
    """
    InvalidImageExtenstion: exception class which represents error of
    image extension. If this exception is arised 400_BAD_REQUEST'll be sent.
    """
    status_code = 400
    default_detail = 'Invalid image extension.'
    default_code = 'invalid_extension'


class BucketDoesNotExist(APIException):
    """
    BucketDoesNotExist: exception class which represents error of
    bucket absense. If this exception is arised 400_BAD_REQUEST'll be sent.
    """
    status_code = 400
    default_detail = 'Bucket does not exist'
    default_code = 'bucket_not_exist'
