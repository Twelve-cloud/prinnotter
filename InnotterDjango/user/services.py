from django.conf import settings
from datetime import datetime, timedelta
import jwt


def generate_token(*, type, user_id):
    """
    generate_token: function which generate corresponding token for user.
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
