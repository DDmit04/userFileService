import datetime
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


@dataclass
class FileRecord(db.Model):
    id: int
    name: str
    extension: str
    size: int
    path: str
    created_at: datetime
    updated_at: datetime
    comment: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False, default=0)
    path = db.Column(db.String, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=0)
    updated_at = db.Column(db.DateTime, default=None)
    comment = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(FileRecord, self).__init__(**kwargs)

    def get_full_filename(self) -> str:
        return self.name + self.extension
