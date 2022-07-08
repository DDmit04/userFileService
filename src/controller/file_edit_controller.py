import uuid

from flask import Blueprint, request, Response
from flask_expects_json import expects_json

from dependency.dependency_container import di_container
from model.requests.request_schemas import file_comment_update_schema, \
    filename_update_schema, filepath_update_schema
from service.file_record_service import FileRecordService
from utils.controller_utils import exception_handle, require_session

file_edit_controller_blueprint = Blueprint('file_edit_controller', __name__)


@file_edit_controller_blueprint.route('<file_id>/comment', methods=["PATCH"])
@exception_handle
@expects_json(file_comment_update_schema)
@require_session
def update_file_comment(session_id: str, file_id: int):
    file_record_service: FileRecordService = di_container\
        .get_file_record_service(session_id)
    new_comment = request.json['comment']
    file_record_service.update_record_comment(file_id, new_comment)
    return Response(status=204)


@file_edit_controller_blueprint.route('<file_id>/name', methods=["PATCH"])
@exception_handle
@expects_json(filename_update_schema)
@require_session
def update_filename(session_id: str, file_id: int):
    new_name = request.json['name']
    file_service_facade = di_container.get_file_service_facade(session_id)
    file_service_facade.update_filename(file_id, new_name)
    return Response(status=204)


@file_edit_controller_blueprint.route('<file_id>/path', methods=["PATCH"])
@exception_handle
@expects_json(filepath_update_schema)
@require_session
def update_file_path(session_id: str, file_id: int):
    new_path = request.json['path']
    file_service_facade = di_container.get_file_service_facade(session_id)
    file_service_facade.update_file_path(file_id, new_path)
    return Response(status=204)
