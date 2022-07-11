import io
from io import BytesIO

import boto3 as boto3
from boto3.resources.base import ServiceResource, ResourceMeta
from botocore.exceptions import ClientError
from werkzeug.datastructures import FileStorage

from repository.file_repo.file_repository import FileRepository


class MinioFileRepository(FileRepository):

    def __init__(self, boto_client: ServiceResource, default_bucket_name: str) \
            -> None:
        super().__init__()
        self._boto_client = boto_client
        self._default_bucket_name = default_bucket_name

    def save_file(self, file: FileStorage, path: str):
        self._boto_client.upload_fileobj(
            file, self._default_bucket_name, path
        )

    def delete_file(self, path: str):
        self._boto_client.delete_object(
            Bucket=self._default_bucket_name, Key=path
        )

    def get_all_files(self):
        pass

    def update_file_path(self, old_file_path: str, new_file_path: str):
        pass

    def update_filename(self, old_file_path: str, new_file_path: str):
        pass

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

