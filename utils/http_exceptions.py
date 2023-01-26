from rest_framework import status
from rest_framework.exceptions import APIException


class AuthenticationHttpException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authorization is not provided or is not valid."
