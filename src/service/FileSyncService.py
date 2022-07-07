import os
import pathlib

from sqlalchemy.orm import Session

from model.FileRecord import FileRecord
from model.dto.AddFileRecordRequest import AddFileRecordRequest
from service.FileRecordService import FileRecordService
from service.FileService import FileService
from service.TransactionableService import TransactionRequiredService
from utils.DatabaseUtills import transactional


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
        all_files_records: list[FileRecord] = self._file_record_service\
            .list_files_records()
        all_real_filepaths = self.__get_real_filepaths(self._upload_dir_path)
        for file_record in all_files_records:
            filename = file_record.name + file_record.extension
            path = file_record.path
            full_path = self._file_service.get_filepath(path, filename)
            exists = all_real_filepaths.count(full_path)
            if exists == 0:
                self._file_record_service.delete_file_record(file_record.id)
            else:
                all_real_filepaths.remove(full_path)
        if len(all_real_filepaths) != 0:
            for full_filepath in all_real_filepaths:
                filename = os.path.basename(full_filepath)
                path_head = self.__get_file_record_path_from_real_path(
                    full_filepath
                )
                name = pathlib.Path(filename).stem
                extension = pathlib.Path(filename).suffix
                size = os.path.getsize(full_filepath)
                addFileRecordRequest = AddFileRecordRequest(
                    name,
                    extension,
                    size,
                    path_head,
                    ''
                )
                self._file_record_service\
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
