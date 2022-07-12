from abc import ABC, abstractmethod


class FileRepository(ABC):

    @abstractmethod
    def save_file(self, file, path: str):
        pass

    @abstractmethod
    def delete_file(self, path: str):
        pass

    @abstractmethod
    def get_all_files_paths(self, from_dir: str):
        pass

    @abstractmethod
    def update_file_path(self, old_file_path: str, new_file_path: str):
        pass

    @abstractmethod
    def update_filename(self, old_file_path: str, new_file_path: str):
        pass

    @abstractmethod
    def check_file_exists(self, filepath: str):
        pass

    @abstractmethod
    def load_file(self, filepath):
        pass
