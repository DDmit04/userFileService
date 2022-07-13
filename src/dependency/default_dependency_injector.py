import os
from typing import Dict

import humanfriendly
from flask import Flask
from sqlalchemy.orm import Session

from dependency.database_session_factory import DatabaseSessionFactory
from repository.file_record_repository import FileRecordRepository
from repository.file_repo.local_file_repository import LocalFileRepository
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.file_service.local_file_service import LocalFileService
from service.file_service_facade import FileServiceFacade
from service.file_sync_service import FileSyncService


class DefaultDependencyInjector:

    def __init__(self):
        super().__init__()
        config = self.get_config()
        db_url: str = config['DB_URL']
        self.database_session_factory = DatabaseSessionFactory(db_url)

    def get_config(self) -> Dict:
        root_dir = os.environ.get('ROOT_DIR', '/')
        upload_dir = os.path.join(
            root_dir,
            os.environ.get('UPLOAD_FOLDER_NAME', '')
        )
        path_separator = os.environ.get('PATH_SEPARATOR', '/')
        db_url = os.getenv('DB_URL')
        max_content_len = humanfriendly.parse_size(
            os.environ.get('MAX_CONTENT_LENGTH', '3M')
        )
        config = {
            'ROOT_DIR': root_dir,
            'PATH_SEPARATOR': path_separator,
            'UPLOAD_DIR_PATH': upload_dir,
            'DB_URL': db_url,
            'MAX_CONTENT_LENGTH': max_content_len
        }
        return config

    def get_file_sync_service(self, session_id: str) -> FileSyncService:
        config = self.get_config()
        upload_dir_path = config['UPLOAD_DIR_PATH']
        path_separator = config['PATH_SEPARATOR']
        return FileSyncService(
            self.get_database_session(session_id),
            upload_dir_path,
            path_separator,
            self.get_file_record_service(session_id),
            self.get_file_service()
        )

    def get_file_service(self) -> FileService:
        config = self.get_config()
        upload_dir_path = config['UPLOAD_DIR_PATH']
        path_separator = config['PATH_SEPARATOR']
        return LocalFileService(
            upload_dir_path,
            path_separator,
            self.get_file_repository()
        )

    def get_file_repository(self):
        return LocalFileRepository()

    def get_file_record_repository(self, session_id):
        return FileRecordRepository(
            self.get_database_session(session_id)
        )

    def get_file_service_facade(self, session_id: str) -> FileServiceFacade:
        return FileServiceFacade(
            self.get_database_session(session_id),
            self.get_file_service(),
            self.get_file_record_service(session_id)
        )

    def get_file_record_service(self, session_id: str) -> FileRecordService:
        config = self.get_config()
        path_separator = config['PATH_SEPARATOR']
        return FileRecordService(
            self.get_database_session(session_id),
            self.get_file_record_repository(session_id),
            path_separator
        )

    def get_flask_app(self) -> Flask:
        config = self.get_config()
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URL']
        app.config['MAX_CONTENT_LENGTH'] = config['MAX_CONTENT_LENGTH']
        app_ctx = app.app_context()
        app_ctx.push()
        return app

    def get_database_session(self, session_id: str) -> Session:
        return self.database_session_factory.get_session(session_id)

    def close_database_session(self, session_id):
        return self.database_session_factory.close_session(session_id)
