from typing import Dict

import boto3
from boto3.resources.base import ServiceResource

from dependency.default_dependency_injector import DefaultDependencyInjector
from repository.file_repo.minio_file_repository import MinioFileRepository
from service.file_service.file_service import FileService
from service.file_service.minio_file_service import MinioFileService


class MinioDependencyInjector(DefaultDependencyInjector):

    def get_config(self) -> Dict:
        config = super().get_config()
        config['UPLOAD_DIR_PATH'] = "/"
        return config

    def get_file_service(self) -> FileService:
        config = self.get_config()
        path_separator = config['PATH_SEPARATOR']
        upload_dir_path = config['UPLOAD_DIR_PATH']
        return MinioFileService(
            upload_dir_path,
            path_separator,
            self.get_file_repository()
        )

    def get_file_repository(self):
        config = self.get_config()
        default_bucket = config['DEFAULT_BUCKET_NAME']
        return MinioFileRepository(self.get_boto_client(), default_bucket)

    def get_boto_client(self) -> ServiceResource:
        config = self.get_config()
        minio_url = config['MINIO_URL']
        s3 = boto3.client('s3', endpoint_url=minio_url)
        return s3
