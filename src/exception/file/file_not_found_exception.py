from exception.error_response_exception import ErrorResponseException


class FileNotFoundException(ErrorResponseException):

    def __init__(self, filepath: str):
        super().__init__(f"Real file by path = {filepath} not found!", 404)
