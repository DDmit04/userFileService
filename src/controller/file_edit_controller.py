import uuid

from flask import Blueprint, request, Response
from flask_expects_json import expects_json

from dependency.dependency_container import di_container
from model.requests.request_schemas import file_comment_update_schema, \
    filename_update_schema, filepath_update_schema
from utils.controller_utils import exception_handle

file_edit_controller_blueprint = Blueprint('file_edit_controller', __name__)


@file_edit_controller_blueprint.route('<file_id>/comment', methods=["PATCH"])
@exception_handle
@expects_json(file_comment_update_schema)
def update_file_comment(file_id: int):
    request_id = str(uuid.uuid1())
    file_record_service: FileRecordService = di_container\
        .get_file_record_service(request_id)
    new_comment = request.json['comment']
    file_record_service.update_record_comment(file_id, new_comment)
    di_container.close_database_session(request_id)
    return Response(status=204)


@file_edit_controller_blueprint.route('<file_id>/name', methods=["PATCH"])
@exception_handle
@expects_json(filename_update_schema)
def update_filename(file_id: int):
    request_id = str(uuid.uuid1())
    new_name = request.json['name']
    file_service_facade = di_container.get_file_service_facade(request_id)
    file_service_facade.update_filename(file_id, new_name)
    di_container.close_database_session(request_id)
    return Response(status=204)


@file_edit_controller_blueprint.route('<file_id>/path', methods=["PATCH"])
@exception_handle
@expects_json(filepath_update_schema)
def update_file_path(file_id: int):
    request_id = str(uuid.uuid1())
    new_path = request.json['path']
    file_service_facade = di_container.get_file_service_facade(request_id)
    file_service_facade.update_file_path(file_id, new_path)
    di_container.close_database_session(request_id)
    return Response(status=204)
