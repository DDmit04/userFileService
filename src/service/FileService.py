import os
import shutil

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.exception.file.FileNotFoundException import FileNotFoundException
from src.exception.file.FileSystemException import FileSystemException
from src.model.FileRecord import FileRecord


class FileService:
    _path_separator: str
    _base_dir: str

    def __init__(self, base_dir, path_separator) -> None:
        super().__init__()
        self._path_separator = path_separator
        self._base_dir = base_dir

    def save_file(self, file: FileStorage, additional_path: str) -> str:
        filename = file.filename
        filename = secure_filename(filename)
        filepath = self.get_filepath(additional_path, filename)
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
        except IOError:
            raise FileSystemException()
        return filepath

    def delete_file(self, file_record: FileRecord):
        additional_path = file_record.path
        filename = file_record.get_full_filename()
        filepath = self.get_filepath_check_exists(additional_path, filename)
        os.remove(filepath)

    def update_filename(self, updated_file_record: FileRecord, new_name: str):
        additional_path = updated_file_record.path
        ext = updated_file_record.extension
        old_filename = updated_file_record.get_full_filename()
        new_filename = new_name + ext
        old_filepath = self.get_filepath_check_exists(additional_path, old_filename)
        new_filepath = self.get_filepath_check_exists(additional_path, new_filename)
        os.rename(old_filepath, new_filepath)

    def update_file_path(self, updated_file_record: FileRecord, new_path: str):
        additional_path = updated_file_record.path
        filename = updated_file_record.get_full_filename()
        old_filepath = self.get_filepath_check_exists(additional_path, filename)
        new_filepath = self.get_filepath_check_exists(new_path, filename)
        os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
        shutil.copy(old_filepath, new_filepath)
        os.remove(old_filepath)

    def get_filepath_check_exists(self, additional_path: str, filename: str) -> str:
        filepath = self.get_filepath(additional_path, filename)
        file_exists = os.path.exists(filepath)
        if not file_exists:
            raise FileNotFoundException(filepath)
        return filepath

    def get_filepath(self, additional_path: str, filename: str) -> str:
        additional_folders = additional_path.split(self._path_separator)
        filepath = self._base_dir
        for additional_folder in additional_folders:
            filepath = os.path.join(filepath, additional_folder)
        filepath = os.path.join(filepath, filename)
        return filepath
