from flask import Blueprint, request, Response, send_file, jsonify
from werkzeug.datastructures import FileStorage

from dependency.DependencyContainer import di_container
from model.FileRecord import FileRecord
from service import FileService, FileRecordService, FileServiceFacade
from utils.ControllerUtils import exception_handle

file_controller_blueprint = Blueprint('file_controller', __name__)


@file_controller_blueprint.route('/', methods=["POST"])
@exception_handle
def add_file():
    file_service_facade: FileServiceFacade = di_container.file_service_facade
    file: FileStorage = request.files['file']
    additional_path_str = request.form['path']
    comment = request.form['comment']
    created_file: FileRecord = file_service_facade.add_file(file, additional_path_str, comment)
    return jsonify(created_file)


@file_controller_blueprint.route('/<file_id>', methods=["DELETE"])
@exception_handle
def delete_file(file_id: int):
    file_service_facade: FileServiceFacade = di_container.file_service_facade
    file_service_facade.delete_file(file_id)
    return Response(status=204)


@file_controller_blueprint.route('/<file_id>/download', methods=["GET"])
@exception_handle
def download_file(file_id: int):
    file_record_service: FileRecordService = di_container.file_record_service
    file_service: FileService = di_container.file_service
    file_record: FileRecord = file_record_service.get_file_record(file_id)
    full_filename = file_record.get_full_filename()
    filepath = file_service.get_filepath_check_exists(
        file_record.path,
        full_filename
    )
    return send_file(filepath, as_attachment=True)
