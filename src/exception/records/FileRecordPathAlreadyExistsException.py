from exception.ErrorResponseException import ErrorResponseException


class FileRecordPathAlreadyExistsException(ErrorResponseException):

    def __init__(self, file_record_path) -> None:
        super().__init__(f"File record with path = {file_record_path} already exists!", 409)
