from exception.error_response_exception import ErrorResponseException


class FileRecordPathAlreadyExistsException(ErrorResponseException):

    def __init__(self, file_record_path: str):
        super().__init__(f"File record with path = {file_record_path} "
                         f"already exists!", 409)
