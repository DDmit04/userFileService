import os
from dataclasses import dataclass

import humanfriendly
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from exception.transaction.SessionNotFoundException import \
    SessionNotFoundException
from model.DatabaseInit import Base
from service.FileRecordService import FileRecordService
from service.FileService import FileService
from service.FileServiceFacade import FileServiceFacade
from service.FileSyncService import FileSyncService

load_dotenv()


@dataclass
class SessionRecord:
    session_id: str
    session: Session


class DependencyInjector:

    def __init__(self):
        super().__init__()
        self.sessions_pool: list[SessionRecord] = []

    def get_config(self):
        root_dir = os.getenv("ROOT_DIR")
        upload_dir = os.path.join(root_dir, os.environ['UPLOAD_FOLDER_NAME'])
        tmp_dir = os.path.join(root_dir, os.getenv('TMP_FOLDER_NAME'))
        path_separator = os.getenv('PATH_SEPARATOR')
        db_url = os.getenv('DB_URL')
        max_content_len = humanfriendly.parse_size(
            os.getenv('MAX_CONTENT_LENGTH'))
        config = {
            'ROOT_DIR': root_dir,
            'PATH_SEPARATOR': path_separator,
            'TMP_DIR_PATH': tmp_dir,
            'UPLOAD_DIR_PATH': upload_dir,
            'DB_URL': db_url,
            'MAX_CONTENT_LENGTH': max_content_len
        }
        return config

    def get_file_sync_service(self, session_id: str) -> FileSyncService:
        config = self.get_config()
        upload_dir_path = config['UPLOAD_DIR_PATH']
        tmp_dir_path = config['TMP_DIR_PATH']
        path_separator = config['PATH_SEPARATOR']
        return FileSyncService(
            self.get_database_session(session_id),
            tmp_dir_path,
            upload_dir_path,
            path_separator,
            self.get_file_record_service(session_id),
            self.get_file_service()
        )

    def get_file_service(self) -> FileService:
        config = self.get_config()
        tmp_dir_path = config['TMP_DIR_PATH']
        upload_dir_path = config['UPLOAD_DIR_PATH']
        path_separator = config['PATH_SEPARATOR']
        return FileService(
            tmp_dir_path,
            upload_dir_path,
            path_separator
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
