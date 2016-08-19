from rest_framework_jwt.settings import api_settings
from datetime import datetime
from calendar import timegm


def jwt_payload_handler(user):
    payload = {
        'user_firstname': user.first_name,
        'user_lastname': user.last_name,
        # 'user_isadmin': user.is_admin,
        'user_id': user.pk,
        'email_address': user.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    return payload
