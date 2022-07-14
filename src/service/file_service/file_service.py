import io
import os
from abc import ABC

from werkzeug.datastructures import FileStorage

from exception.file.file_not_found_exception import FileNotFoundException
from model.dto.stored_fIle_stats_dto import StoredFileStatsDto
from model.file_record import FileRecord
from repository.file_repo.file_repository import FileRepository


class FileService(ABC):

    def __init__(self,
                 upload_dir: str,
                 path_separator: str,
                 file_repository: FileRepository):
        super().__init__()
        self.path_separator = path_separator
        self.upload_dir = upload_dir
        self.file_repository = file_repository

    def save_file(self, file: FileStorage, additional_path: str) -> str:
        new_filepath = self.get_filepath(
            additional_path,
            file.filename
        )
        self.file_repository.save_file(file, new_filepath)

    def delete_file(self, additional_path: str, filename: str):
        filepath = self.get_filepath_check_exists(additional_path, filename)
        self.file_repository.delete_file(filepath)

    def update_filename(self, updated_file_record: FileRecord, new_name: str):
        additional_path = updated_file_record.path
        ext = updated_file_record.extension
        old_filename = updated_file_record.get_full_filename()
        new_filename = new_name + ext
        old_filepath = self.get_filepath_check_exists(
            additional_path,
            old_filename
        )
        new_filepath = self.get_filepath(additional_path, new_filename)
        self.file_repository.update_filename(old_filepath, new_filepath)

    def update_file_path(self, updated_file_record: FileRecord, new_path: str):
        additional_path = updated_file_record.path
        filename = updated_file_record.get_full_filename()
        old_filepath = self.get_filepath_check_exists(additional_path,
                                                      filename)
        new_filepath = self.get_filepath(new_path, filename)
        self.file_repository.update_file_path(old_filepath, new_filepath)

    def get_filepath_check_exists(self, additional_path: str, filename: str) \
            -> str:
        filepath = self.get_filepath(additional_path, filename)
        file_exists = self.file_repository.check_file_exists(filepath)
        if not file_exists:
            raise FileNotFoundException(filepath)
        return filepath

    def get_filepath(self, additional_path: str, filename: str) -> str:
        additional_folders = additional_path.split(self.path_separator)
        filepath = self.upload_dir
        for additional_folder in additional_folders:
            filepath = os.path.join(filepath, additional_folder)
        filepath = os.path.join(filepath, filename)
        return filepath

    def get_file(self, path: str, full_filename: str) -> io.BytesIO:
        filepath = self.get_filepath_check_exists(path, full_filename)
        file = self.file_repository.load_file(filepath)
        return file

    def get_all_filepaths(self, upload_dir_path: str) -> list[str]:
        return self.file_repository.get_all_files_paths(upload_dir_path)

    def get_file_stats_by_path(self, real_file_path: str) -> \
            StoredFileStatsDto:
        return self.file_repository.get_file_stats(real_file_path)
