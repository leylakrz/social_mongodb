import jwt

from social.settings import SECRET_KEY, logger
from user_profile.queries import check_user_name_exists
from utils.http_exceptions import AuthenticationHttpException


def generate_access_token(user_name):
    payload = {
        "user_name": user_name,
    }
    return jwt_encode(payload)


def jwt_encode(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def jwt_decode(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as error:
        logger.error(f"{type(error)}: {str(error)}")
        raise AuthenticationHttpException()


class JWTAuthentication:

    def authenticate(self, request):
        access_token = request.headers.get('Authorization', None)
        token_payload = self.get_token_payload(access_token)
        return (self.get_user_name(token_payload), access_token)

    def get_token_payload(self, token):
        if token:
            return jwt_decode(token)
        raise AuthenticationHttpException()

    def get_user_name(self, payload):
        user_name = payload.get("user_name")
        if user_name and check_user_name_exists(user_name):
            return user_name
        raise AuthenticationHttpException()
