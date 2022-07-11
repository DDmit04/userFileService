import os

from werkzeug.datastructures import FileStorage

from exception.file.file_not_found_exception import FileNotFoundException
from exception.file.file_system_exception import FileSystemException
from model.file_record import FileRecord
from repository.file_repo.file_repository import FileRepository
from service.file_service.file_service import FileService


class LocalFileService(FileService):

    def __init__(self, tmp_dir: str, upload_dir: str, path_separator: str,
                 file_repository: FileRepository):
        super().__init__(tmp_dir, upload_dir, path_separator, file_repository)

    def save_file(self, file: FileStorage, additional_path: str) -> str:
        try:
            return super().save_file(file, additional_path)
        except IOError:
            raise FileSystemException()

    def delete_file(self, additional_path: str, filename: str):
        super().delete_file(additional_path, filename)
        self.clean_up_dirs(self.upload_dir)

    def update_file_path(self, updated_file_record: FileRecord, new_path: str):
        super().update_file_path(updated_file_record, new_path)
        self.clean_up_dirs(self.upload_dir)

    def clean_up_dirs(self, dir_path: str):
        files = os.listdir(dir_path)
        if len(files) > 0:
            for file in files:
                full_path = os.path.join(dir_path, file)
                isdir = os.path.isdir(full_path)
                if isdir:
                    self.clean_up_dirs(full_path)
        files = os.listdir(dir_path)
        if len(files) == 0 and dir_path != self.upload_dir:
            os.rmdir(dir_path)
