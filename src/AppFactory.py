import os
import pathlib

from flask import current_app, jsonify, make_response
from jsonschema.exceptions import ValidationError
from sqlalchemy.orm import Session

from controller.FileController import file_controller_blueprint
from controller.FileEditController import file_edit_controller_blueprint
from controller.FileRecordController import file_record_controller_blueprint
from model.FileRecord import db, FileRecord
from model.dto.AddFileRecordRequest import AddFileRecordRequest
from repos.FileRecordRepository import FileRecordRepository
from service.FileRecordService import FileRecordService
from service.FileService import FileService
from service.FileServiceFacade import FileServiceFacade


def setup_app(app):
    app_ctx = app.app_context()
    app_ctx.push()

    db.init_app(app)
    db.create_all()

    file_repo = FileRecordRepository()
    file_record_service = FileRecordService()
    file_service = FileService()
    file_service_facade = FileServiceFacade()

    current_app.file_record_service = file_record_service
    current_app.file_service = file_service
    current_app.file_service_facade = file_service_facade
    current_app.file_repo = file_repo
    current_app.db = db

    app.register_blueprint(file_controller_blueprint, url_prefix='/file')
    app.register_blueprint(file_record_controller_blueprint, url_prefix='/file/info')
    app.register_blueprint(file_edit_controller_blueprint, url_prefix='/file/edit')

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return make_response(jsonify({'error': original_error.message}), 400)
        return error

    session: Session = db.session
    refresh_data_before_start(session, app.config)

    return app


def refresh_data_before_start(session: Session, app_config):
    base_dir = app_config['UPLOAD_FOLDER']
    path_separator = current_app.config['PATH_SEPARATOR']
    file_record_service: FileRecordService = current_app.file_record_service
    file_service: FileService = current_app.file_service
    all_files_records: list[FileRecord] = session.query(FileRecord).all()
    all_real_filepaths = get_real_filepaths(base_dir)
    for file_record in all_files_records:
        filename = file_record.name + file_record.extension
        path = file_record.path
        full_path = file_service.get_filepath(base_dir, path, filename)
        exists = all_real_filepaths.count(full_path)
        if exists == 0:
            file_record_service.delete_file_record(file_record.id)
        else:
            all_real_filepaths.remove(full_path)
    if len(all_real_filepaths) != 0:
        for full_filepath in all_real_filepaths:
            filename = os.path.basename(full_filepath)
            path_head = get_file_record_path_from_real_path(base_dir, path_separator, full_filepath)
            name = pathlib.Path(filename).stem
            extension = pathlib.Path(filename).suffix
            size = os.path.getsize(full_filepath)
            addFileRecordRequest = AddFileRecordRequest(name, extension, size, path_head, '')
            file_record_service.add_new_file_record(addFileRecordRequest)


def get_file_record_path_from_real_path(base_dir, separator, real_filepath):
    path = real_filepath.replace(base_dir, '')
    path = os.path.normpath(path)
    path_elements = path.split(os.sep)
    path = separator.join(path_elements)
    path_head = os.path.split(path)[0]
    return path_head


def get_real_filepaths(dir_path):
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(os.path.join(dir_path, path))
        else:
            res += get_real_filepaths(os.path.join(dir_path, path))
    return res
