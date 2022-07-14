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

    def __init__(self, **kwargs):
        super(FileRecord, self).__init__(**kwargs)

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
