from datetime import datetime

from sqlalchemy.orm import Session

from exception.records.file_record_path_already_exists_exception import \
    FileRecordPathAlreadyExistsException
from model.dto.add_file_record_request import AddFileRecordRequest
from model.file_record import FileRecord
from repository.file_record_repository import FileRecordRepository
from service.transaction_required_service import TransactionRequiredService
from utils.data_utils import create_new_file_record
from utils.database_utills import transactional


class FileRecordService(TransactionRequiredService):

    def __init__(self,
                 session: Session,
                 file_record_repo: FileRecordRepository,
                 path_separator: str):
        super().__init__(session)
        self._file_record_repo = file_record_repo
        self._path_separator = path_separator

    @transactional
    def add_new_file_record(self,
                            add_file_record_request: AddFileRecordRequest,
                            creation_time: datetime,
                            update_time: datetime) -> FileRecord:
        new_file_record: FileRecord = create_new_file_record(
            add_file_record_request,
            creation_time,
            update_time
        )
        return self.__add_file_record(new_file_record)

    @transactional
    def add_new_file_record_by_request(self,
                                       add_file_record_request:
                                       AddFileRecordRequest) -> FileRecord:
        new_file_record: FileRecord = create_new_file_record(
            add_file_record_request)
        return self.__add_file_record(new_file_record)

    @transactional
    def delete_file_record(self, file_id: int):
        self._file_record_repo.delete_file_record_by_id(file_id)

    @transactional
    def list_files_records(self) -> list[FileRecord]:
        file_records = self._file_record_repo.get_all_files_records()
        return file_records

    @transactional
    def get_file_record(self, file_id: int) -> FileRecord:
        file_record = self._file_record_repo.get_file_record_by_id(file_id)
        return file_record

    @transactional
    def update_record_comment(self, file_id: int, new_comment: str):
        update_dict = {FileRecord.comment: new_comment}
        self.__update_record(file_id, update_dict)

    @transactional
    def update_record_name(self, file_id: int, new_name: str):
        update_dict = {FileRecord.name: new_name}
        self.__update_record(file_id, update_dict)

    @transactional
    def update_record_path(self, file_id: int, new_path: str):
        update_dict = {FileRecord.path: new_path}
        self.__update_record(file_id, update_dict)

    @transactional
    def get_records_on_dir(self, dir_level: str) -> list[FileRecord]:
        dir_level = self.secure_additional_path(dir_level)
        file_records = self._file_record_repo.get_file_records_with_path(
            dir_level
        )
        return file_records

    @transactional
    def get_record_by_id(self, file_id: int) -> FileRecord:
        file_record = self._file_record_repo.get_file_record_by_id(file_id)
        return file_record

    def secure_additional_path(self, path: str):
        path_separator = self._path_separator
        if not path.startswith(path_separator):
            path = f'/{path}'
        if path.endswith(path_separator):
            path = path[:-1]
        return path

    def __update_record(self, file_id, update_dict):
        current_date = datetime.now()
        current_date_iso = current_date.isoformat()
        update_dict.update({
            FileRecord.updated_at: current_date_iso
        })
        self._file_record_repo.update_file_record(file_id, update_dict)

    def __add_file_record(self, new_file_record: FileRecord) -> FileRecord:
        filename = new_file_record.name
        file_ext = new_file_record.extension
        file_path = new_file_record.path
        existing_file = self._file_record_repo.find_record_by_full_path(
            file_path,
            filename,
            file_ext
        )
        if existing_file is not None:
            raise FileRecordPathAlreadyExistsException(
                f"{file_path}/{filename}{file_ext}")
        else:
            self._file_record_repo.save_file_record(new_file_record)
            return new_file_record
