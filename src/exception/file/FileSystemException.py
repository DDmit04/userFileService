from exception.ErrorResponseException import ErrorResponseException


class FileSystemException(ErrorResponseException):

    def __init__(self):
        super().__init__("IO server error!", 500)



