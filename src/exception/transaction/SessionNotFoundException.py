from exception.ErrorResponseException import ErrorResponseException


class SessionNotFoundException(ErrorResponseException):
    def __init__(self) -> None:
        super().__init__(f"Database session error!", 500)