from exception.ErrorResponseException import ErrorResponseException


class FileRecordIdNotFoundException(ErrorResponseException):

    def __init__(self, file_record_id) -> None:
        super().__init__(f"File record with id = {file_record_id} not found!", 404)
