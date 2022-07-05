import os
import shutil

from flask import current_app
from werkzeug.utils import secure_filename

from exception.file.FileNotFoundException import FileNotFoundException
from exception.file.FileSystemException import FileSystemException
from model.FileRecord import FileRecord


class FileService:

    def save_file(self, file, base_dir, additional_path):
        filename = file.filename
        filename = secure_filename(filename)
        filepath = self.get_filepath(base_dir, additional_path, filename)
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
        except IOError:
            raise FileSystemException()
        return filepath

    def delete_file(self, base_dir, file_record: FileRecord):
        additional_path = file_record.path
        filename = file_record.get_full_filename()
        filepath = self.get_filepath(base_dir, additional_path, filename)
        os.remove(filepath)

    def update_filename(self, base_dir, updated_file_record: FileRecord, new_name):
        additional_path = updated_file_record.path
        ext = updated_file_record.extension
        old_filename = updated_file_record.get_full_filename()
        new_filename = new_name + ext
        old_filepath = self.get_filepath(base_dir, additional_path, old_filename)
        new_filepath = self.get_filepath(base_dir, additional_path, new_filename)
        os.rename(old_filepath, new_filepath)

    def update_file_path(self, base_dir, updated_file_record: FileRecord, new_path):
        additional_path = updated_file_record.path
        filename = updated_file_record.get_full_filename()
        old_filepath = self.get_filepath(base_dir, additional_path, filename)
        new_filepath = self.get_filepath(base_dir, new_path, filename)
        os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
        shutil.copy(old_filepath, new_filepath)
        os.remove(old_filepath)

    def get_filepath(self, base_dir, additional_path, filename):
        path_separator = current_app.config['PATH_SEPARATOR']
        additional_folders = additional_path.split(path_separator)
        filepath = base_dir
        for additional_folder in additional_folders:
            filepath = os.path.join(filepath, additional_folder)
        filepath = os.path.join(filepath, filename)
        file_exists = os.path.exists(filepath)
        if not file_exists:
            raise FileNotFoundException(filepath)
        return filepath
