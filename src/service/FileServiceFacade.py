import pathlib

from flask import current_app

from utils.DataabseUtils import transactional
from model.dto.AddFileRecordRequest import AddFileRecordRequest
from service.FileRecordService import FileRecordService
from service.FileService import FileService


class FileServiceFacade:

    @transactional
    def add_file(self, file, additional_path_str, comment):
        file_service: FileService = current_app.file_service
        file_record_service: FileRecordService = current_app.file_record_service
        filename = file.filename
        name = pathlib.Path(filename).stem
        extension = pathlib.Path(filename).suffix
        size = len(file.read())
        addFileRecordRequest = AddFileRecordRequest(name, extension, size, additional_path_str, comment)
        created_file = file_record_service.add_new_file_record(addFileRecordRequest)
        base_dir = current_app.config['UPLOAD_FOLDER']
        file_service.save_file(file, base_dir, additional_path_str)
        return created_file

    @transactional
    def delete_file(self, file_id):
        file_record_service: FileRecordService = current_app.file_record_service
        file_service: FileService = current_app.file_service
        file_to_delete_info = file_record_service.get_file_record(file_id)
        file_record_service.delete_file_record(file_id)
        base_dir = current_app.config['UPLOAD_FOLDER']
        file_service.delete_file(base_dir, file_to_delete_info)

