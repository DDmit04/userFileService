import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from service.FileRecordService import FileRecordService
from service.FileService import FileService
from service.FileServiceFacade import FileServiceFacade
from service.FileSyncService import FileSyncService

from RootDir import ROOT_DIR

load_dotenv()


class DependencyInjector:
    app: Flask
    database: SQLAlchemy
    file_service: FileService
    file_record_service: FileRecordService
    file_service_facade: FileServiceFacade
    file_sync_service: FileSyncService

    def __init__(self, database) -> None:
        super().__init__()
        self.setup_app()
        self.setup_database(database)
        upload_dir = os.path.join(ROOT_DIR, os.getenv('UPLOAD_FOLDER_NAME'))
        path_separator = os.getenv('PATH_SEPARATOR')
        self.file_service = FileService(upload_dir, path_separator)
        self.file_record_service = FileRecordService(database)
        self.file_sync_service = FileSyncService(database, upload_dir, path_separator, self.file_record_service, self.file_service)
        self.file_service_facade = FileServiceFacade(database, self.file_service, self.file_record_service)

    def setup_database(self, database):
        database.init_app(self.app)
        database.create_all()
        self.database = database

    def setup_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
        app_ctx = self.app.app_context()
        app_ctx.push()