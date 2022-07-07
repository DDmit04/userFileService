import uuid

from flask import Blueprint, request, Response, send_file, jsonify
from werkzeug.datastructures import FileStorage

from dependency.DependencyContainer import di_container
from exception.ErrorResponseException import ErrorResponseException
from model.FileRecord import FileRecord
from service import FileService, FileRecordService, FileServiceFacade
from utils.ControllerUtils import exception_handle

file_controller_blueprint = Blueprint('file_controller', __name__)


@file_controller_blueprint.route('/', methods=["POST"])
@exception_handle
def add_file():
    file: FileStorage = request.files.get('file', None)
    if file is not None:
        request_id = str(uuid.uuid1())
        file_service_facade = di_container.get_file_service_facade(request_id)
        additional_path_str = request.form['path']
        comment = request.form['comment']
        created_file: FileRecord = file_service_facade.add_file(
            file,
            additional_path_str,
            comment
        )
        di_container.close_database_session(request_id)
        return jsonify(created_file)
    else:
        raise ErrorResponseException('File is empty!', 400)


@file_controller_blueprint.route('/<file_id>', methods=["DELETE"])
@exception_handle
def delete_file(file_id: int):
    request_id = str(uuid.uuid1())
    file_service_facade: FileServiceFacade = di_container\
        .get_file_service_facade(request_id)
    file_service_facade.delete_file(file_id)
    di_container.close_database_session(request_id)
    return Response(status=204)


@file_controller_blueprint.route('/<file_id>/download', methods=["GET"])
@exception_handle
def download_file(file_id: int):
    request_id = str(uuid.uuid1())
    file_record_service: FileRecordService = \
        di_container.get_file_record_service(request_id)
    file_service: FileService = di_container.get_file_service()
    file_record: FileRecord = file_record_service.get_record(file_id)
    full_filename = file_record.get_full_filename()
    filepath = file_service.get_filepath_check_exists(
        file_record.path,
        full_filename
    )
    di_container.close_database_session(request_id)
    return send_file(filepath, as_attachment=True)
