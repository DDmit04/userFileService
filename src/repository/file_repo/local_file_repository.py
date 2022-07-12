import os
import shutil
from io import BytesIO

from werkzeug.datastructures import FileStorage

from repository.file_repo.file_repository import FileRepository


class LocalFileRepository(FileRepository):

    def save_file(self, file: FileStorage, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)

    def delete_file(self, path: str):
        os.remove(path)

    def get_all_files_paths(self, from_dir):
        res = []
        if not os.path.exists(from_dir):
            return []
        for path in os.listdir(from_dir):
            if os.path.isfile(os.path.join(from_dir, path)):
                res.append(os.path.join(from_dir, path))
            else:
                res += self.get_all_files_paths(
                    os.path.join(from_dir, path))
        return res

    def update_file_path(self, old_file_path: str, new_file_path: str):
        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        shutil.copy(old_file_path, new_file_path)
        os.remove(old_file_path)

    def update_filename(self, old_file_path: str, new_file_path: str):
        os.rename(old_file_path, new_file_path)

    def check_file_exists(self, filepath: str) -> bool:
        file_exists = os.path.exists(filepath)
        return file_exists

    def load_file(self, filepath):
        with open(filepath, "rb") as file:
            buf = BytesIO(file.read())
            return buf
