from flask import Blueprint, current_app, request
from flask_expects_json import expects_json

from model.FileRecord import FileRecord
from model.requests.RequestSchemas import file_comment_update_schema, filename_update_schema, filepath_update_schema
from service.FileRecordService import FileRecordService
from service.FileService import FileService
from utils.ControllerUtils import exception_handle

file_edit_controller_blueprint = Blueprint('file_edit_controller', __name__)


@file_edit_controller_blueprint.route('<file_id>/comment', methods=["PATCH"])
@exception_handle
@expects_json(file_comment_update_schema)
def get_files_list(file_id):
    file_record_service: FileRecordService = current_app.file_record_service
    new_comment = request.json['comment']
    updated_file_record: FileRecord = file_record_service.update_file_comment(file_id, new_comment)
    return updated_file_record.as_dict()


@file_edit_controller_blueprint.route('<file_id>/name', methods=["PATCH"])
@exception_handle
@expects_json(filename_update_schema)
def get_file(file_id):
    file_record_service: FileRecordService = current_app.file_record_service
    file_service: FileService = current_app.file_service
    new_name = request.json['name']
    file_record_to_update = file_record_service.get_file_record(file_id)
    file_service.update_filename(current_app.config['UPLOAD_FOLDER'], file_record_to_update, new_name)
    file_record_to_update = file_record_service.update_file_name(file_id, new_name)
    return file_record_to_update.as_dict()


@file_edit_controller_blueprint.route('<file_id>/path', methods=["PATCH"])
@exception_handle
@expects_json(filepath_update_schema)
def add_file(file_id):
    file_record_service: FileRecordService = current_app.file_record_service
    file_service: FileService = current_app.file_service
    new_path = request.json['path']
    file_record_to_update = file_record_service.get_file_record(file_id)
    file_service.update_file_path(current_app.config['UPLOAD_FOLDER'], file_record_to_update, new_path)
    file_record_to_update = file_record_service.update_file_path(file_id, new_path)
    return file_record_to_update.as_dict()
