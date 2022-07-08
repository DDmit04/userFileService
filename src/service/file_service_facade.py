from sqlalchemy.orm import Session
from werkzeug.datastructures import FileStorage

from model.dto.add_file_record_request import AddFileRecordRequest
from model.dto.fIle_stats_dto import FileStatsDto
from model.file_record import FileRecord
from service.file_record_service import FileRecordService
from service.file_service import FileService
from service.transaction_required_service import TransactionRequiredService
from utils.database_utills import transactional


class FileServiceFacade(TransactionRequiredService):

    def __init__(self, session: Session,
                 file_service: FileService,
                 file_record_service: FileRecordService):
        super().__init__(session)
        self._file_service = file_service
        self._file_record_service = file_record_service

    @transactional
    def add_file(self, file: FileStorage, additional_path_str: str, comment: str):
        additional_path_str = self._file_record_service.secure_additional_path(
            additional_path_str
        )
        fileStats: FileStatsDto = self._file_service.get_tmp_file_stats(file)
        addFileRecordRequest: AddFileRecordRequest = AddFileRecordRequest(
            fileStats.filename,
            fileStats.ext,
            fileStats.size,
            additional_path_str,
            comment)
        created_file: FileRecord = self._file_record_service\
            .add_new_file_record_by_request(addFileRecordRequest)
        self._file_service.save_file(fileStats, additional_path_str)
        return created_file

    @transactional
    def delete_file(self, file_id: int):
        file_to_delete_info: FileRecord = self._file_record_service\
            .get_record_by_id(file_id)
        additional_path = file_to_delete_info.path
        full_filename = file_to_delete_info.get_full_filename()
        self._file_record_service.delete_file_record(file_id)
        self._file_service.delete_file(additional_path, full_filename)

    @transactional
    def update_filename(self, file_id: int, new_name: str) -> FileRecord:
        file_record_to_update: FileRecord = self._file_record_service\
            .get_record_by_id(file_id)
        self._file_service.update_filename(file_record_to_update, new_name)
        file_record_to_update = self._file_record_service\
            .update_record_name(file_id, new_name)
        return file_record_to_update

    @transactional
    def update_file_path(self, file_id: int, new_path: str) -> FileRecord:
        new_path = self._file_record_service.secure_additional_path(new_path)
        file_record_to_update: FileRecord = self._file_record_service\
            .get_record_by_id(file_id)
        self._file_service.update_file_path(file_record_to_update, new_path)
        file_record_to_update = self._file_record_service\
            .update_record_path(file_id, new_path)
        return file_record_to_update
