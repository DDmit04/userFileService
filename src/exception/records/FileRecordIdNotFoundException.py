from exception.ErrorResponseException import ErrorResponseException


class FileRecordIdNotFoundException(ErrorResponseException):

    def __init__(self, file_record_id: int):
        super().__init__(f"File record with id = {file_record_id} "
                         f"not found!", 404)
