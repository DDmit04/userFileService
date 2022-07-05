class AddFileRecordRequest:
    name = ''
    extension = ''
    size = 0
    path = ''
    comment = ''

    def __init__(self, name, extension, size, path, comment) -> None:
        super().__init__()
        self.name = name
        self.extension = extension
        self.size = size
        self.path = path
        self.comment = comment
