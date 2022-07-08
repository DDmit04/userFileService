import uuid

from dependency.dependency_container import di_container
from exception.error_response_exception import ErrorResponseException


def exception_handle(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except ErrorResponseException as e:
            return {'message': e.message}, e.status_code

    wrapper.__name__ = func.__name__
    return wrapper


def require_session(func):
    def wrapper(*args, **kwargs):
        session_id = str(uuid.uuid1())
        di_container.get_database_session(session_id)
        try:
            res = func(session_id, *args, **kwargs)
        finally:
            di_container.close_database_session(session_id)
        return res

    wrapper.__name__ = func.__name__
    return wrapper
