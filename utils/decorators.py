from functools import wraps
from bson.errors import InvalidId
from rest_framework.exceptions import NotFound


def invalid_id_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidId:
            raise NotFound

    return wrapper
