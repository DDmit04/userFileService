import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, DateTime

from model.database_init import Base


@dataclass
class FileRecord(Base):
    __tablename__ = 'file_record'
    id: int
    name: str
    extension: str
    size: int
    path: str
    created_at: datetime
    updated_at: datetime
    comment: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Integer, nullable=False, default=0)
    path = Column(String, nullable=False, default=0)
    created_at = Column(DateTime, default=0)
    updated_at = Column(DateTime, default=None)
    comment = Column(String, nullable=False)

    def __init__(self, rec_id: int,
                 name: str,
                 extension: str,
                 size: int,
                 path: str,
                 created_at: datetime,
                 updated_at: datetime,
                 comment: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = rec_id
        self.name = name
        self.extension = extension
        self.size = size
        self.path = path
        self.created_at = created_at
        self.updated_at = updated_at
        self.comment = comment

    def get_full_filename(self) -> str:
        return self.name + self.extension

    def __hash__(self):
        return hash((self.id, self.name, self.extension, self.path))

    def __eq__(self, other):
        try:
            return (self.id, self.name, self.extension, self.path) \
                   == (other.id, other.name, other.extension, other.path)
        except AttributeError:
            return NotImplemented
