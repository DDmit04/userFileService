from dataclasses import dataclass


@dataclass
class ErrorResponseException(BaseException):
    message: str = ''
    status_code: int = 500

