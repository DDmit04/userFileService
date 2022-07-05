from dataclasses import dataclass


@dataclass
class AddFileRecordRequest:
    name: str = ''
    extension: str = ''
    size: int = 0
    path: str = ''
    comment: str = ''
