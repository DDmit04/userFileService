from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db: SQLAlchemy = SQLAlchemy()

class FileRecord(db.Model, SerializerMixin):
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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_full_filename(self):
        return self.name + self.extension
