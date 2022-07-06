import pathlib

from werkzeug.datastructures import FileStorage

from src.model.FileRecord import FileRecord
from src.model.dto.AddFileRecordRequest import AddFileRecordRequest
from src.service.FileRecordService import FileRecordService
from src.service.FileService import FileService
from src.service.TransactionableService import TransactionRequiredService
from src.utils.DatabaseUtills import transactional


class FileServiceFacade(TransactionRequiredService):
    _file_service: FileService
    _file_record_service: FileRecordService

    def __init__(self, database, file_service, file_record_service) -> None:
        super().__init__(database)
        self._file_service = file_service
        self._file_record_service = file_record_service

    @transactional
    def add_file(self, file: FileStorage, additional_path_str: str, comment: str):
        filename = file.filename
        name = pathlib.Path(filename).stem
        extension = pathlib.Path(filename).suffix
        size = len(file.read())
        addFileRecordRequest: AddFileRecordRequest = AddFileRecordRequest(name, extension, size, additional_path_str,
                                                                          comment)
        created_file: FileRecord = self._file_record_service.add_new_file_record(addFileRecordRequest)
        self._file_service.save_file(file, additional_path_str)
        return created_file

    @transactional
    def delete_file(self, file_id: int):
        file_record_service: FileRecordService = self._file_record_service
        file_service: FileService = self._file_service
        file_to_delete_info: FileRecord = file_record_service.get_file_record(file_id)
        file_record_service.delete_file_record(file_id)
        file_service.delete_file(file_to_delete_info)
