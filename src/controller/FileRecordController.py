import uuid

from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json

from dependency.DependencyContainer import di_container
from model import FileRecord
from model.requests.RequestSchemas import file_level_search_schema
from service import FileRecordService
from utils.ControllerUtils import exception_handle

file_record_controller_blueprint = Blueprint('file_record_controller', __name__)


@file_record_controller_blueprint.route('/', methods=["GET"])
@exception_handle
def get_file_records_list():
    request_id = str(uuid.uuid1())
    file_record_service: FileRecordService = di_container\
        .get_file_record_service(request_id)
    file_records = file_record_service.list_files_records()
    response = jsonify(file_records)
    di_container.close_database_session(request_id)
    return response


@file_record_controller_blueprint.route('/<file_id>', methods=["GET"])
@exception_handle
def get_file_record(file_id: int):
    request_id = str(uuid.uuid1())
    file_record_service: FileRecordService = di_container\
        .get_file_record_service(request_id)
    file_record: FileRecord = file_record_service.get_record(file_id)
    response = jsonify(file_record)
    di_container.close_database_session(request_id)
    return response


@file_record_controller_blueprint.route('/level', methods=["GET"])
@exception_handle
@expects_json(file_level_search_schema)
def get_file_records_by_dir():
    request_id = str(uuid.uuid1())
    file_record_service: FileRecordService = di_container\
        .get_file_record_service(request_id)
    dir_level = request.json['level']
    file_records: list[FileRecord] = file_record_service\
        .get_records_on_dir(dir_level)
    response = jsonify(file_records)
    di_container.close_database_session(request_id)
    return response

