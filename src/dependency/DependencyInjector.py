import os

from dotenv import load_dotenv
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

from src.service.FileRecordService import FileRecordService
from src.service.FileService import FileService
from src.service.FileServiceFacade import FileServiceFacade
from src.service.FileSyncService import FileSyncService

load_dotenv()


class DependencyInjector:
    app: Flask
    database: SQLAlchemy
    file_service: FileService
    file_record_service: FileRecordService
    file_service_facade: FileServiceFacade
    file_sync_service: FileSyncService
    config = {}

    def __init__(self, database) -> None:
        super().__init__()
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
        app_ctx = self.app.app_context()
        app_ctx.push()
        database.init_app(self.app)
        database.create_all()
        self.database = database
        upload_dir = os.getenv('UPLOAD_FOLDER_PATH')
        path_separator = os.getenv('PATH_SEPARATOR')
        self.config = {
            'UPLOAD_FOLDER': upload_dir,
            'PATH_SEPARATOR': path_separator
        }
        self.file_service = FileService(upload_dir, path_separator)
        self.file_record_service = FileRecordService(database)
        self.file_sync_service = FileSyncService(database, upload_dir, path_separator, self.file_record_service, self.file_service)
        self.file_service_facade = FileServiceFacade(database, self.file_service, self.file_record_service)
