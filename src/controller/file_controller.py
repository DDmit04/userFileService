import uuid

from flask import Blueprint, request, Response, send_file, jsonify
from werkzeug.datastructures import FileStorage

from dependency.dependency_container import di_container
from exception.error_response_exception import ErrorResponseException
from model.file_record import FileRecord
from service.file_record_service import FileRecordService
from service.file_service import FileService
from service.file_service_facade import FileServiceFacade
from utils.controller_utils import exception_handle, require_session

file_controller_blueprint = Blueprint('file_controller', __name__)


@file_controller_blueprint.route('/', methods=["POST"])
@exception_handle
@require_session
def add_file(session_id: str):
    file: FileStorage = request.files.get('file', None)
    if file is not None:
        file_service_facade = di_container.get_file_service_facade(session_id)
        additional_path_str = request.form['path']
        comment = request.form['comment']
        created_file: FileRecord = file_service_facade.add_file(
            file,
            additional_path_str,
            comment
        )
        response = jsonify(created_file)
        return response
    else:
        raise ErrorResponseException('File is empty!', 400)


@file_controller_blueprint.route('/<file_id>', methods=["DELETE"])
@exception_handle
@require_session
def delete_file(session_id: str, file_id: int):
    file_service_facade: FileServiceFacade = di_container\
        .get_file_service_facade(session_id)
    file_service_facade.delete_file(file_id)
    return Response(status=204)


@file_controller_blueprint.route('/<file_id>/download', methods=["GET"])
@exception_handle
@require_session
def download_file(session_id: str, file_id: int):
    file_record_service: FileRecordService = \
        di_container.get_file_record_service(session_id)
    file_service: FileService = di_container.get_file_service()
    file_record: FileRecord = file_record_service.get_record_by_id(file_id)
    full_filename = file_record.get_full_filename()
    filepath = file_service.get_filepath_check_exists(
        file_record.path,
        full_filename
    )
    return send_file(filepath, as_attachment=True)
