from datetime import datetime
from typing import Dict

from flask import current_app

from src.exception.records.FileRecordPathAlreadyExistsException import FileRecordPathAlreadyExistsException
from src.model.FileRecord import FileRecord
from src.model.dto.AddFileRecordRequest import AddFileRecordRequest
from src.repos.FileRecordRepository import FileRecordRepository
from src.utils.DataabseUtils import transactional


class FileRecordService:

    @transactional
    def add_new_file_record(self, add_file_record_request: AddFileRecordRequest) -> FileRecord:
        new_file: FileRecord = self.__create_new_file_record(add_file_record_request)
        file_record_repo: FileRecordRepository = current_app.file_repo
        filename = new_file.name
        file_ext = new_file.extension
        file_path = new_file.path
        existing_file: FileRecord = file_record_repo.get_file_record_by_path(file_path, filename, file_ext)
        if existing_file is not None:
            raise FileRecordPathAlreadyExistsException(f"{file_path}/{filename}.{file_ext}")
        else:
            saved_file: FileRecord = file_record_repo.save_file(new_file)
            return saved_file

    @transactional
    def delete_file_record(self, file_id: int):
        current_app.file_repo.delete_file(file_id)

    @transactional
    def list_files_records(self) -> list[FileRecord]:
        files = current_app.file_repo.get_all_files()
        return files

    @transactional
    def get_file_record(self, file_id: int) -> FileRecord:
        file = current_app.file_repo.get_file(file_id)
        return file

    @transactional
    def update_file_comment(self, file_id: int, new_comment: str) -> FileRecord:
        return self.__update_file_info(file_id, {FileRecord.comment: new_comment})

    @transactional
    def update_file_name(self, file_id: int, new_name: str) -> FileRecord:
        return self.__update_file_info(file_id, {FileRecord.name: new_name})

    @transactional
    def update_file_path(self, file_id: int, new_path: str) -> FileRecord:
        return self.__update_file_info(file_id, {FileRecord.path: new_path})

    @transactional
    def get_file_records_on_level(self, dir_level: str) -> list[FileRecord]:
        file_records = current_app.file_repo.get_file_records_by_dir(dir_level)
        return file_records

    def __update_file_info(self, file_id: int, update_dict: Dict) -> FileRecord:
        file = current_app.file_repo.update_file(file_id, update_dict)
        return file

    def __create_new_file_record(self, add_file_record_request: AddFileRecordRequest) -> FileRecord:
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
