import io

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError
from werkzeug.datastructures import FileStorage

from repository.file_repo.file_repository import FileRepository


class MinioFileRepository(FileRepository):

    def __init__(self, boto_client: ServiceResource, default_bucket_name: str):
        super().__init__()
        self._boto_client = boto_client
        self._default_bucket_name = default_bucket_name

    def save_file(self, file: FileStorage, path: str):
        self._boto_client.upload_fileobj(
            file, self._default_bucket_name, path
        )

    def delete_file(self, path: str):
        self._boto_client.delete_object(
            Bucket=self._default_bucket_name,
            Key=path
        )

    def get_all_files_paths(self, from_dir: str) -> list[str]:
        response = self._boto_client.list_objects(
            Bucket=self._default_bucket_name,
            Prefix=from_dir
        )
        result = response.get('Contents', [])
        all_filepaths = list(map(lambda content: content['Key'], result))
        return all_filepaths

    def update_file_path(self, old_file_path: str, new_file_path: str):
        self.__move_file(old_file_path, new_file_path)

    def update_filename(self, old_file_path: str, new_file_path: str):
        self.__move_file(old_file_path, new_file_path)

    def check_file_exists(self, filepath: str):
        try:
            self._boto_client.head_object(
                Bucket=self._default_bucket_name, Key=filepath
            )
        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                return False
            else:
                raise e
        return True

    def load_file(self, filepath) -> io.BytesIO:
        file = io.BytesIO()
        self._boto_client.download_fileobj(
            self._default_bucket_name, filepath, file
        )
        return file

    def __move_file(self, old_file_path: str, new_file_path: str):
        copy_source = {
            'Bucket': self._default_bucket_name,
            'Key': old_file_path
        }
        self._boto_client.copy_object(
            Bucket=self._default_bucket_name,
            CopySource=copy_source,
            Key=new_file_path
        )
        self._boto_client.delete_object(
            Bucket=self._default_bucket_name,
            Key=old_file_path
        )
