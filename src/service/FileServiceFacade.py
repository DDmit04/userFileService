import pathlib

from flask import current_app
from werkzeug.datastructures import FileStorage

from src.model.FileRecord import FileRecord
from src.model.dto.AddFileRecordRequest import AddFileRecordRequest
from src.service.FileRecordService import FileRecordService
from src.service.FileService import FileService
from src.utils.DataabseUtils import transactional


class FileServiceFacade:

    @transactional
    def add_file(self, file: FileStorage, additional_path_str: str, comment: str):
        file_service: FileService = current_app.file_service
        file_record_service: FileRecordService = current_app.file_record_service
        filename = file.filename
        name = pathlib.Path(filename).stem
        extension = pathlib.Path(filename).suffix
        size = len(file.read())
        addFileRecordRequest: AddFileRecordRequest = AddFileRecordRequest(name, extension, size, additional_path_str, comment)
        created_file: FileRecord = file_record_service.add_new_file_record(addFileRecordRequest)
        # TODO remove
        base_dir = current_app.config['UPLOAD_FOLDER']
        file_service.save_file(file, base_dir, additional_path_str)
        return created_file

    @transactional
    def delete_file(self, file_id: int):
        file_record_service: FileRecordService = current_app.file_record_service
        file_service: FileService = current_app.file_service
        file_to_delete_info: FileRecord = file_record_service.get_file_record(file_id)
        file_record_service.delete_file_record(file_id)
        # TODO remove
        base_dir = current_app.config['UPLOAD_FOLDER']
        file_service.delete_file(base_dir, file_to_delete_info)

