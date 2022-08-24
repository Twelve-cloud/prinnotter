from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import status
from django.conf import settings
from user.models import User
import jwt


def generate_token(*, type, user_id):
    """
    generate_token: generates corresponding token for user.
    Parameters:
        1) type - type of the token. It can be 'access' or 'refresh'.
           If none of these types will be passed it raises an exception.
        2) user_id - user identifier. It's required because user_id is
           included by payload for authorization and authentication.
    """
    if type == 'access':
        lifetime = timedelta(
            minutes=settings.JWT_TOKEN['ACCESS_TOKEN_LIFETIME_MINUTES']
        )
    elif type == 'refresh':
        lifetime = timedelta(
            days=settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS']
        )
    else:
        raise ValueError('Unexpected type of token: must be access or refresh')

    expiry_token_date = datetime.now() + lifetime
    payload = {
        'id': user_id,
        'exp': int(expiry_token_date.strftime('%s'))
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def set_tokens_to_cookie(response, user_id):
    """
    set_token_to_cookie: set token to cookie to response object.
    """
    response.set_cookie(
        key='access_token',
        value=generate_token(type='access', user_id=user_id),
        secure=settings.JWT_TOKEN['SECURE'],
        httponly=settings.JWT_TOKEN['HTTP_ONLY']
    )

    response.set_cookie(
        key='refresh_token',
        value=generate_token(type='refresh', user_id=user_id),
        secure=settings.JWT_TOKEN['SECURE'],
        httponly=settings.JWT_TOKEN['HTTP_ONLY']
    )


def get_payload_by_token(token):
    """
    get_payload_by_token: returns payload of decoding token.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        settings.JWT_TOKEN['ALGORITHMS']
    )


def get_new_tokens(request, refresh_token):
    """
    get_new_refresh_token: returns new refresh token if it's not expired
    otherwise returns bad request.
    """
    try:
        payload = get_payload_by_token(refresh_token)
        request.user = User.objects.get(pk=payload.get('id'))

        response = create_response(
            data={'Tokens': 'OK'},
            status=status.HTTP_200_OK
        )
        set_tokens_to_cookie(response, request.user.id)

        return response

    except jwt.ExpiredSignatureError:
        return create_response(
            data={'Refresh Token': 'Expired'},
            status=status.HTTP_400_BAD_REQUEST,
            hdrs={'WWW-Authenticate': 'Sign in again'}
        )
        # If front-end will get 400_BAD_REQUEST
        # It will remove refresh token from cookie
        # and request to /auth/jwt/sign_in
        # without any tokens in a cookie


def create_response(data, status, rndr=None, mtype=None, cntx=None, hdrs=None):
    """
    create_response: creates and renders response object from rest_framework.
    """
    response = Response(data=data, status=status)
    response.accepted_renderer = rndr if rndr else JSONRenderer()
    response.accepted_media_type = mtype if mtype else 'application/json'
    response.renderer_context = cntx if cntx else {}

    for header in (hdrs or []):
        response.headers[header] = hdrs[header]

    response.render()
    return response
