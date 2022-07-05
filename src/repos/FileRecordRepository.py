from datetime import datetime

from flask import current_app
from sqlalchemy.orm import Session

from exception.records.FileRecordIdNotFoundException import FileRecordIdNotFoundException
from model.FileRecord import FileRecord


class FileRecordRepository:

    def save_file(self, file):
        session: Session = current_app.db.session
        session.add(file)
        return file

    def delete_file(self, file_id):
        session: Session = current_app.db.session
        session.query(FileRecord).filter(FileRecord.id == file_id).delete()

    def get_file(self, file_id):
        session: Session = current_app.db.session
        file = session.query(FileRecord).filter(FileRecord.id == file_id).first()
        if file is None:
            raise FileRecordIdNotFoundException(file_id)
        return file

    def get_all_files(self):
        session: Session = current_app.db.session
        files = session.query(FileRecord).all()
        return files

    def update_file(self, file_id, update_dict):
        current_date = datetime.now()
        current_date_iso = current_date.isoformat()
        update_dict.update({
            FileRecord.updated_at: current_date_iso
        })
        file = self.get_file(file_id)
        session: Session = current_app.db.session
        session.query(FileRecord).filter(FileRecord.id == file_id).update(update_dict)
        return file

    def get_file_record_by_path(self, path, name, ext):
        session: Session = current_app.db.session
        file = session.query(FileRecord).filter(FileRecord.path == path,
                                                FileRecord.name == name,
                                                FileRecord.extension == ext).first()
        return file

    def get_file_records_by_dir(self, dir_level):
        session: Session = current_app.db.session
        file_records = session.query(FileRecord).filter(FileRecord.path.contains(dir_level)).all()
        return file_records
