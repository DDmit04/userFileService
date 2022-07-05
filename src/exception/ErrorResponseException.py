class ErrorResponseException(BaseException):
    message = ''
    status_code = 500

    def __init__(self, message, status) -> None:
        super().__init__()
        self.message = message
        self.status_code = status

