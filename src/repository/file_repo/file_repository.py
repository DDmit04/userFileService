import io
from abc import ABC, abstractmethod

from model.dto.stored_fIle_stats_dto import StoredFileStatsDto


class FileRepository(ABC):

    @abstractmethod
    def save_file(self, file, path: str):
        pass

    @abstractmethod
    def delete_file(self, path: str):
        pass

    @abstractmethod
    def get_all_files_paths(self, from_dir: str) -> list[str]:
        pass

    @abstractmethod
    def update_file_path(self, old_file_path: str, new_file_path: str):
        pass

    @abstractmethod
    def update_filename(self, old_file_path: str, new_file_path: str):
        pass

    @abstractmethod
    def check_file_exists(self, filepath: str) -> bool:
        pass

    @abstractmethod
    def load_file(self, filepath) -> io.BytesIO:
        pass

    @abstractmethod
    def get_file_stats(self, real_file_path) -> StoredFileStatsDto:
        pass
