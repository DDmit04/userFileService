from datetime import datetime

from sqlalchemy.orm import Session

from exception.records.file_recordId_not_found_exception import \
    FileRecordIdNotFoundException
from model.file_record import FileRecord


class FileRecordRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save_file_record(self, file_record: FileRecord) -> FileRecord:
        self.session.add(file_record)

    def find_record_by_full_path(self, file_path: str, filename: str,
                                 ext: str) -> FileRecord:
        existing_file: FileRecord = self.session \
            .query(FileRecord) \
            .filter(
                FileRecord.path == file_path,
                FileRecord.name == filename,
                FileRecord.extension == ext
            ).first()
        return existing_file

    def delete_file_record_by_id(self, file_id: int):
        self.session \
            .query(FileRecord) \
            .filter(FileRecord.id == file_id) \
            .delete()

    def get_all_files_records(self) -> list[FileRecord]:
        files = self.session.query(FileRecord).all()
        return files

    def get_file_record_by_id(self, file_id: int) -> FileRecord:
        file_record = self.session \
            .query(FileRecord) \
            .filter(FileRecord.id == file_id) \
            .first()
        if file_record is None:
            raise FileRecordIdNotFoundException(file_id)
        return file_record

    def get_file_records_with_path(self, path):
        file_records = self.session \
            .query(FileRecord) \
            .filter(FileRecord.path.startswith(path)) \
            .all()
        return file_records

    def update_file_record(self, file_id, update_dict):
        current_date = datetime.now()
        current_date_iso = current_date.isoformat()
        update_dict.update({
            FileRecord.updated_at: current_date_iso
        })
        self.session \
            .query(FileRecord) \
            .filter(FileRecord.id == file_id) \
            .update(update_dict)
