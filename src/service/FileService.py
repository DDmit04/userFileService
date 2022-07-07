import os
import pathlib
import shutil

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from exception.file.FileNotFoundException import FileNotFoundException
from exception.file.FileSystemException import FileSystemException
from model.FileRecord import FileRecord

from model.dto.FIleStatsDto import FileStatsDto


class FileService:
    _path_separator: str
    _base_dir: str
    _tmp_dir: str

    def __init__(self, tmp_dir, upload_dir, path_separator) -> None:
        super().__init__()
        self._tmp_dir = tmp_dir
        self._path_separator = path_separator
        self._base_dir = upload_dir

    def save_file(self, file_stats: FileStatsDto, additional_path: str) -> str:
        new_filepath = self.get_filepath(additional_path, file_stats.get_full_filename())
        try:
            os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
            full_tmp_path = file_stats.full_path
            shutil.copy(full_tmp_path, new_filepath)
            os.remove(full_tmp_path)
        except IOError:
            raise FileSystemException()
        return new_filepath

    def delete_file(self, additional_path: str, filename: str):
        filepath = self.get_filepath_check_exists(additional_path, filename)
        os.remove(filepath)
        self.clean_up_dirs(self._base_dir)

    def update_filename(self, updated_file_record: FileRecord, new_name: str):
        additional_path = updated_file_record.path
        ext = updated_file_record.extension
        old_filename = updated_file_record.get_full_filename()
        new_filename = new_name + ext
        old_filepath = self.get_filepath_check_exists(additional_path, old_filename)
        new_filepath = self.get_filepath(additional_path, new_filename)
        os.rename(old_filepath, new_filepath)

    def update_file_path(self, updated_file_record: FileRecord, new_path: str):
        additional_path = updated_file_record.path
        filename = updated_file_record.get_full_filename()
        old_filepath = self.get_filepath_check_exists(additional_path, filename)
        new_filepath = self.get_filepath(new_path, filename)
        os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
        shutil.copy(old_filepath, new_filepath)
        os.remove(old_filepath)
        self.clean_up_dirs(self._base_dir)

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

    def get_tmp_file_stats(self, file: FileStorage) -> FileStatsDto:
        filepath = self.save_file_to_tmp_dir(file)
        size = os.stat(filepath).st_size
        filename = file.filename
        name = pathlib.Path(filename).stem
        extension = pathlib.Path(filename).suffix
        file_stats_dto = FileStatsDto(name, extension, size, filepath)
        return file_stats_dto

    def save_file_to_tmp_dir(self, file) -> str:
        tmp_dir = self._tmp_dir
        filepath = os.path.join(tmp_dir, file.filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        return filepath

    def clean_up_dirs(self, dir_path: str):
        files = os.listdir(dir_path)
        if len(files) > 0:
            for file in files:
                full_path = os.path.join(dir_path, file)
                isdir = os.path.isdir(full_path)
                if isdir:
                    self.clean_up_dirs(full_path)
        files = os.listdir(dir_path)
        if len(files) == 0 and dir_path is not self._base_dir:
            os.rmdir(dir_path)
