import os
import pathlib

from sqlalchemy.orm import Session

from model.dto.add_file_record_request import AddFileRecordRequest
from model.file_record import FileRecord
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.transaction_required_service import TransactionRequiredService
from utils.database_utills import transactional


class FileSyncService(TransactionRequiredService):

    def __init__(self,
                 session: Session,
                 upload_dir_path: str,
                 path_separator: str,
                 file_record_service: FileRecordService,
                 file_service: FileService):
        super().__init__(session)
        self._upload_dir_path = upload_dir_path
        self._path_separator = path_separator
        self._file_record_service = file_record_service
        self._file_service = file_service

    @transactional
    def sync_storage_data(self):
        all_files_records: list[FileRecord] = \
            self._file_record_service.list_files_records()
        real_files_paths = self._file_service.get_all_filepaths(
            self._upload_dir_path
        )
        real_files_paths = self.__remove_orphan_file_records(
            all_files_records,
            real_files_paths
        )
        if len(real_files_paths) != 0:
            self.__add_existing_files_records(real_files_paths)

    def __add_existing_files_records(self, real_files_paths):
        for real_file_path in real_files_paths:
            record_filename = os.path.basename(real_file_path)
            file_dir = self.__get_file_record_path_from_real_path(
                real_file_path
            )
            name = pathlib.Path(record_filename).stem
            extension = pathlib.Path(record_filename).suffix
            file_stats = self._file_service \
                .get_file_stats_by_path(real_file_path)
            size = file_stats.size
            last_updated = file_stats.updated
            created = file_stats.created
            addFileRecordRequest = AddFileRecordRequest(
                name, extension,
                size, file_dir
            )
            self._file_record_service.add_new_file_record(
                addFileRecordRequest,
                created,
                last_updated
            )

    def __remove_orphan_file_records(self, all_files_records, real_files_paths):
        for file_record in all_files_records:
            record_filename = file_record.name + file_record.extension
            record_path = file_record.path
            record_full_path = self._file_service.get_filepath(
                record_path,
                record_filename
            )
            real_file_exists = real_files_paths.count(record_full_path) == 1
            if not real_file_exists:
                record_id = file_record.id
                self._file_record_service.delete_file_record(record_id)
            else:
                real_files_paths.remove(record_full_path)
        return real_files_paths

    def __get_file_record_path_from_real_path(self, real_filepath: str) -> str:
        path = real_filepath
        if real_filepath.startswith(self._upload_dir_path):
            path = real_filepath.replace(self._upload_dir_path, '', 1)
        path = os.path.normpath(path)
        path_elements = path.split(os.sep)
        path = self._path_separator.join(path_elements)
        path_head = os.path.split(path)[0]
        return path_head
