from datetime import datetime
from typing import Dict

from sqlalchemy.orm import Session

from exception.records.FileRecordIdNotFoundException import \
    FileRecordIdNotFoundException
from exception.records.FileRecordPathAlreadyExistsException import \
    FileRecordPathAlreadyExistsException
from model.FileRecord import FileRecord
from model.dto.AddFileRecordRequest import AddFileRecordRequest
from service.TransactionableService import TransactionRequiredService
from utils.DatabaseUtills import transactional


class FileRecordService(TransactionRequiredService):

    def __init__(self, session: Session, path_separator: str):
        super().__init__(session)
        self._path_separator = path_separator

    @transactional
    def add_new_file_record(self,
                            add_file_record_request: AddFileRecordRequest) -> FileRecord:
        new_file: FileRecord = self.__create_new_record(
            add_file_record_request)
        filename = new_file.name
        file_ext = new_file.extension
        file_path = new_file.path
        existing_file: FileRecord = self.session.query(FileRecord).filter(
            FileRecord.path == file_path,
            FileRecord.name == filename,
            FileRecord.extension == file_ext).first()
        if existing_file is not None:
            raise FileRecordPathAlreadyExistsException(
                f"{file_path}/{filename}{file_ext}")
        else:
            self.session.add(new_file)
            return new_file

    @transactional
    def delete_file_record(self, file_id: int):
        self.session.query(FileRecord).filter(FileRecord.id ==
                                              file_id).delete()

    @transactional
    def list_files_records(self) -> list[FileRecord]:
        files = self.session.query(FileRecord).all()
        return files

    @transactional
    def get_file_record(self, file_id: int) -> FileRecord:
        file = self.get_record(file_id)
        return file

    @transactional
    def update_record_comment(self, file_id: int, new_comment: str) \
            -> FileRecord:
        return self.__update_record_info(
            file_id,
            {FileRecord.comment: new_comment})

    @transactional
    def update_record_name(self, file_id: int, new_name: str) -> FileRecord:
        return self.__update_record_info(file_id, {FileRecord.name: new_name})

    @transactional
    def update_record_path(self, file_id: int, new_path: str) -> FileRecord:
        return self.__update_record_info(file_id, {FileRecord.path: new_path})

    @transactional
    def get_records_on_dir(self, dir_level: str) -> list[FileRecord]:
        file_records = self.session.query(FileRecord) \
            .filter(FileRecord.path.startswith(dir_level)) \
            .all()
        return file_records

    def __update_record_info(self, file_id: int, update_dict: Dict) \
            -> FileRecord:
        current_date = datetime.now()
        current_date_iso = current_date.isoformat()
        update_dict.update({
            FileRecord.updated_at: current_date_iso
        })
        file = self.get_record(file_id)
        self.session.query(FileRecord) \
            .filter(FileRecord.id == file_id) \
            .update(update_dict)
        return file

    def get_record(self, file_id) -> FileRecord:
        file = self.session.query(FileRecord) \
            .filter(FileRecord.id == file_id) \
            .first()
        if file is None:
            raise FileRecordIdNotFoundException(file_id)
        return file

    def secure_additional_path(self, path: str):
        path_separator = self._path_separator
        if not path.startswith(path_separator):
            path = f'/{path}'
        if path.endswith(path_separator):
            path = path[:-1]
        return path

    def __create_new_record(self,
                            add_file_record_request: AddFileRecordRequest) \
            -> FileRecord:
        current_date = datetime.now()
        current_date_iso = current_date.isoformat()
        new_file: FileRecord = FileRecord(
            name=add_file_record_request.name,
            extension=add_file_record_request.extension,
            size=add_file_record_request.size,
            path=add_file_record_request.path,
            created_at=current_date_iso,
            comment=add_file_record_request.comment
        )
        return new_file
