from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required

from dependency.dependency_container import di_container
from model.file_record import FileRecord
from model.requests.request_schemas import file_level_search_schema
from service.file_record_service import FileRecordService
from utils.controller_utils import exception_handle, require_session

file_record_controller_blueprint = Blueprint('file_record_controller',
                                             __name__)


@file_record_controller_blueprint.route('/', methods=["GET"])
@jwt_required()
@exception_handle
@require_session
def get_file_records_list(session_id: str):
    file_record_service: FileRecordService = di_container \
        .get_file_record_service(session_id)
    file_records = file_record_service.list_files_records()
    response = jsonify(file_records)
    return response


@file_record_controller_blueprint.route('/<file_id>', methods=["GET"])
@jwt_required()
@exception_handle
@require_session
def get_file_record(session_id: str, file_id: int):
    file_record_service: FileRecordService = di_container \
        .get_file_record_service(session_id)
    file_record: FileRecord = file_record_service.get_record_by_id(file_id)
    response = jsonify(file_record)
    return response


@file_record_controller_blueprint.route('/level', methods=["GET"])
@jwt_required()
@exception_handle
@expects_json(file_level_search_schema)
@require_session
def get_file_records_by_dir(session_id: str):
    file_record_service: FileRecordService = di_container \
        .get_file_record_service(session_id)
    dir_level = request.json['level']
    file_records: list[FileRecord] = file_record_service \
        .get_records_on_dir(dir_level)
    response = jsonify(file_records)
    return response
