from exception.ErrorResponseException import ErrorResponseException


class SessionNotFoundException(ErrorResponseException):
    def __init__(self):
        super().__init__(f"Database session error!", 500)