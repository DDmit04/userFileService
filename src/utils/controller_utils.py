from exception.error_response_exception import ErrorResponseException


def exception_handle(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except ErrorResponseException as e:
            return {'message': e.message}, e.status_code

    wrapper.__name__ = func.__name__
    return wrapper
