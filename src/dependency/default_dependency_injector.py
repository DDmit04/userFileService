import os
from dataclasses import dataclass
from typing import Dict

import boto3
import humanfriendly
from boto3.resources.base import ServiceResource
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from exception.transaction.session_not_found_exception import \
    SessionNotFoundException
from model.database_init import Base
from repository.file_record_repository import FileRecordRepository
from repository.file_repo.local_file_repository import LocalFileRepository
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.file_service.local_file_service import LocalFileService
from service.file_service_facade import FileServiceFacade
from service.file_sync_service import FileSyncService


@dataclass
class SessionRecord:
    session_id: str
    session: Session


class DefaultDependencyInjector:

    def __init__(self):
        super().__init__()
        self.sessions_pool: list[SessionRecord] = []

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

    def get_boto_client(self) -> ServiceResource:
        config = self.get_config()
        minio_url = config['MINIO_URL']
        s3 = boto3.client('s3', endpoint_url=minio_url)
        return s3

    def get_flask_app(self) -> Flask:
        config = self.get_config()
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URL']
        app.config['MAX_CONTENT_LENGTH'] = config['MAX_CONTENT_LENGTH']
        app_ctx = app.app_context()
        app_ctx.push()
        return app

    def get_database_session(self, session_id: str) -> Session:
        existing_session_record: SessionRecord = self \
            .__find_session_by_id(session_id)
        if existing_session_record is None:
            session = self.__create_new_database_session()
            self.sessions_pool.append(SessionRecord(session_id, session))
            session.begin()
            return session
        return existing_session_record.session

    def close_database_session(self, session_id):
        existing_session_record: SessionRecord = self \
            .__find_session_by_id(session_id)
        if existing_session_record is None:
            raise SessionNotFoundException()
        session: Session = existing_session_record.session
        session.commit()
        session.close()
        self.sessions_pool.remove(existing_session_record)

    def __create_new_database_session(self) -> Session:
        config = self.get_config()
        db_url: str = config['DB_URL']
        engine: str = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine)
        session_maker: sessionmaker = sessionmaker(bind=engine)
        session: Session = session_maker()
        return session

    def __find_session_by_id(self, session_id) -> SessionRecord:
        for existing_session in self.sessions_pool:
            if existing_session.session_id == session_id:
                return existing_session
        return None
