from dataclasses import dataclass


@dataclass
class AddFileRecordRequest:
    name: str = ''
    extension: str = ''
    size: int = 0
    path: str = ''
    comment: str = ''

    def __init__(self, name: str,
                 extension: str,
                 size: int,
                 path: str,
                 comment: str = ''):
        super().__init__()
        self.name = name
        self.extension = extension
        self.size = size
        self.path = path
        self.comment = comment


