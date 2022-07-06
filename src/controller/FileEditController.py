from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json

from src.dependency.DependencyContainer import di_container
from src.model import FileRecord
from src.model.requests.RequestSchemas import file_comment_update_schema, filename_update_schema, filepath_update_schema
from src.service import FileRecordService
from src.utils.ControllerUtils import exception_handle

file_edit_controller_blueprint = Blueprint('file_edit_controller', __name__)


@file_edit_controller_blueprint.route('<file_id>/comment', methods=["PATCH"])
@exception_handle
@expects_json(file_comment_update_schema)
def update_file_comment(file_id: int):
    file_record_service: FileRecordService = di_container.file_record_service
    new_comment = request.json['comment']
    updated_file_record: FileRecord = file_record_service.update_file_comment(file_id, new_comment)
    return jsonify(updated_file_record)


@file_edit_controller_blueprint.route('<file_id>/name', methods=["PATCH"])
@exception_handle
@expects_json(filename_update_schema)
def update_filename(file_id: int):
    new_name = request.json['name']
    file_service_facade = di_container.file_service_facade
    updated_record = file_service_facade.update_filename(file_id, new_name)
    return jsonify(updated_record)


@file_edit_controller_blueprint.route('<file_id>/path', methods=["PATCH"])
@exception_handle
@expects_json(filepath_update_schema)
def update_file_path(file_id: int):
    new_path = request.json['path']
    file_service_facade = di_container.file_service_facade
    updated_record = file_service_facade.update_file_path(file_id, new_path)
    return jsonify(updated_record)
