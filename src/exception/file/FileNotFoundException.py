from src.exception.ErrorResponseException import ErrorResponseException


class FileNotFoundException(ErrorResponseException):

    def __init__(self, filepath: str) -> None:
        super().__init__(f"Real file by path = {filepath} not found!", 404)
