import os
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
        boto_url = os.environ.get("BOTO_URL", '')
        boto_profile = os.environ.get("BOTO_PROFILE", 'default')
        default_bucket_name = os.environ.get("DEFAULT_BUCKET_NAME", 'default')
        config.update({
            'BOTO_URL': boto_url,
            'BOTO_PROFILE': boto_profile,
            'DEFAULT_BUCKET_NAME': default_bucket_name
        })
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
        boto_url = config['BOTO_URL']
        boto_profile = config['BOTO_PROFILE']
        session = boto3.Session(profile_name=boto_profile)
        client = session.client('s3', endpoint_url=boto_url)
        return client
