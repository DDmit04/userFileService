import datetime
from dataclasses import dataclass

from src.model.DatabaseInit import database


@dataclass
class FileRecord(database.Model):
    id: int
    name: str
    extension: str
    size: int
    path: str
    created_at: datetime
    updated_at: datetime
    comment: str

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    extension = database.Column(database.String, nullable=False)
    size = database.Column(database.Integer, nullable=False, default=0)
    path = database.Column(database.String, nullable=False, default=0)
    created_at = database.Column(database.DateTime, default=0)
    updated_at = database.Column(database.DateTime, default=None)
    comment = database.Column(database.String, nullable=False)

    def __init__(self, **kwargs):
        super(FileRecord, self).__init__(**kwargs)

    def get_full_filename(self) -> str:
        return self.name + self.extension
