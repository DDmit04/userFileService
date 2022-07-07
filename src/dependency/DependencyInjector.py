import os
from typing import Dict

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from service.FileRecordService import FileRecordService
from service.FileService import FileService
from service.FileServiceFacade import FileServiceFacade
from service.FileSyncService import FileSyncService

load_dotenv()


class DependencyInjector:

    def __init__(self, database: SQLAlchemy):
        super().__init__()
        self.setup_app()
        self.setup_database(database)
        root_dir = os.getenv("ROOT_DIR")
        upload_dir = os.path.join(root_dir, os.getenv('UPLOAD_FOLDER_NAME'))
        tmp_dir = os.path.join(root_dir, os.getenv('TMP_DIR_NAME'))
        path_separator = os.getenv('PATH_SEPARATOR')
        self.config = {
            'ROOT_DIR': root_dir,
            'PATH_SEPARATOR': path_separator,
            'TMP_DIR_NAME': tmp_dir,
            'UPLOAD_FOLDER_NAME': upload_dir
        }
        self.file_service = FileService(tmp_dir, upload_dir, path_separator)
        self.file_record_service = FileRecordService(database, path_separator)
        self.file_sync_service = FileSyncService(
            database,
            upload_dir,
            path_separator,
            self.file_record_service,
            self.file_service
        )
        self.file_service_facade = FileServiceFacade(
            database,
            self.file_service,
            self.file_record_service
        )

    def setup_database(self, database):
        database.init_app(self.app)
        database.create_all()
        self.database = database

    def setup_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
        app_ctx = self.app.app_context()
        app_ctx.push()
