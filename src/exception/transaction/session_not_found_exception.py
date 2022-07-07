from exception.error_response_exception import ErrorResponseException


class SessionNotFoundException(ErrorResponseException):
    def __init__(self):
        super().__init__(f"Database session error!", 500)