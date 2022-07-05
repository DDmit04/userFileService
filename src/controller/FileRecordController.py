from flask import Blueprint, current_app, jsonify, request
from flask_expects_json import expects_json

from model.requests.RequestSchemas import file_level_search_schema
from service.FileRecordService import FileRecordService
from utils.ControllerUtils import exception_handle

file_record_controller_blueprint = Blueprint('file_record_controller', __name__)


@file_record_controller_blueprint.route('/', methods=["GET"])
@exception_handle
def get_file_records_list():
    file_record_service: FileRecordService = current_app.file_record_service
    file_records = file_record_service.list_files_records()
    return jsonify([file.as_dict() for file in file_records])


@file_record_controller_blueprint.route('/<file_id>', methods=["GET"])
@exception_handle
def get_file_record(file_id):
    file_record_service: FileRecordService = current_app.file_record_service
    file = file_record_service.get_file_record(file_id)
    return file.as_dict()


@file_record_controller_blueprint.route('/level', methods=["GET"])
@exception_handle
@expects_json(file_level_search_schema)
def get_file_records_by_dir():
    file_record_service: FileRecordService = current_app.file_record_service
    dir_level = request.json['level']
    file_records = file_record_service.get_file_records_on_level(dir_level)
    return jsonify([file.as_dict() for file in file_records])

