from rest_framework.exceptions import APIException


class InvalidFilterType(APIException):
    status_code = 400
    default_detail = 'Invalid filter type.'
    default_code = 'invalid_type'
