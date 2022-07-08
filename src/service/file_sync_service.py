import os
import pathlib

from sqlalchemy.orm import Session

from model.dto.add_file_record_request import AddFileRecordRequest
from model.file_record import FileRecord
from service.file_record_service import FileRecordService
from service.file_service import FileService
from service.transaction_required_service import TransactionRequiredService
from utils.database_utills import transactional


class FileSyncService(TransactionRequiredService):

    def __init__(self,
                 session: Session,
                 tmp_dir_filepath,
                 upload_dir_path: str,
                 path_separator: str,
                 file_record_service: FileRecordService,
                 file_service: FileService):
        super().__init__(session)
        self._tmp_dir_path = tmp_dir_filepath
        self._upload_dir_path = upload_dir_path
        self._path_separator = path_separator
        self._file_record_service = file_record_service
        self._file_service = file_service

    @transactional
    def sync_storage_data(self):
        all_files_records: list[FileRecord] = self._file_record_service \
            .list_files_records()
        real_files_paths = self.__get_real_filepaths(self._upload_dir_path)
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
        if len(real_files_paths) != 0:
            for real_file_path in real_files_paths:
                record_filename = os.path.basename(real_file_path)
                file_dir = self.__get_file_record_path_from_real_path(
                    real_file_path
                )
                name = pathlib.Path(record_filename).stem
                extension = pathlib.Path(record_filename).suffix
                size = os.path.getsize(real_file_path)
                addFileRecordRequest = AddFileRecordRequest(
                    name, extension,
                    size, file_dir, ''
                )
                self._file_record_service \
                    .add_new_file_record(addFileRecordRequest)
        self._file_service.clean_up_dirs(self._upload_dir_path)

    def clean_up_tmp_dir(self):
        for path in os.listdir(self._tmp_dir_path):
            os.remove(os.path.join(self._tmp_dir_path, path))

    def __get_file_record_path_from_real_path(self, real_filepath: str) -> str:
        path = real_filepath.replace(self._upload_dir_path, '')
        path = os.path.normpath(path)
        path_elements = path.split(os.sep)
        path = self._path_separator.join(path_elements)
        path_head = os.path.split(path)[0]
        return path_head

    def __get_real_filepaths(self, dir_path: str):
        res = []
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(os.path.join(dir_path, path))
            else:
                res += self.__get_real_filepaths(os.path.join(dir_path, path))
        return res
