from botocore.exceptions import ClientError
from werkzeug.datastructures import FileStorage

from exception.file.file_system_exception import FileSystemException
from repository.file_repo.file_repository import FileRepository
from service.file_service.file_service import FileService


class MinioFileService(FileService):

    def __init__(self,
                 upload_dir: str,
                 path_separator: str,
                 file_repository: FileRepository):
        super().__init__(upload_dir, path_separator, file_repository)

    def save_file(self, file: FileStorage, additional_path: str) -> str:
        try:
            return super().save_file(file, additional_path)
        except ClientError:
            raise FileSystemException()

