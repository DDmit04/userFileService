import unittest
from unittest import mock
from unittest.mock import Mock

from sqlalchemy.orm import Session, SessionTransaction
from werkzeug.datastructures import FileStorage

from model.dto.add_file_record_request import AddFileRecordRequest
from model.file_record import FileRecord
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.file_service_facade import FileServiceFacade
from utils.data_utils import create_test_file_record


class FileServiceFacadeTest(unittest.TestCase):

    def setUp(self):
        self.__session = Mock(spec=Session)
        self.__session_transaction = Mock(spec=SessionTransaction)
        self.__session.begin_nested.return_value = self.__session_transaction
        self.__file_record_service = Mock(spec=FileRecordService)
        self.__file_service = Mock(spec=FileService)
        self.__file_sync_service = FileServiceFacade(
            self.__session,
            self.__file_record_service,
            self.__file_service
        )

    def __get_test_file_records(self):
        expected_records = []
        for i in range(5):
            file_record = create_test_file_record(i)
            expected_records.append(file_record)
        return expected_records

    def __create_add_file_record_request(self) -> AddFileRecordRequest:
        request = AddFileRecordRequest()
        request.name = 'name'
        request.extension = '.ext'
        request.size = 100
        request.path = self.__path_separator.join(['path', 'dir'])
        request.comment = 'comment'
        return request

    def add_file(self):
        additional_path = '/dir/path'
        comment = 'comment'
        file_data = 'data'
        file_encoding = "ascii"
        mocked_open_function = mock.mock_open(
            read_data=file_data.encode(file_encoding)
        )
        with mock.patch("builtins.open", mocked_open_function):
            with open("any filepath") as f:
                file = FileStorage(f)
        fileStats = get_file_stats(file)
        addFileRecordRequest: AddFileRecordRequest = AddFileRecordRequest(
            fileStats.filename,
            fileStats.ext,
            fileStats.size,
            additional_path_str,
            comment)
        created_file = self._file_record_service \
            .add_new_file_record_by_request(addFileRecordRequest)
        self._file_service.save_file(
            file,
            additional_path_str
        )
        return created_file

    def delete_file(self, file_id: int):
        file_to_delete_info: FileRecord = self._file_record_service \
            .get_record_by_id(file_id)
        additional_path = file_to_delete_info.path
        full_filename = file_to_delete_info.get_full_filename()
        self._file_record_service.delete_file_record(file_id)
        self._file_service.delete_file(additional_path, full_filename)

    def update_filename(self, file_id: int, new_name: str) -> FileRecord:
        file_record_to_update: FileRecord = self._file_record_service \
            .get_record_by_id(file_id)
        self._file_service.update_filename(file_record_to_update, new_name)
        file_record_to_update = self._file_record_service \
            .update_record_name(file_id, new_name)
        return file_record_to_update

    def update_file_path(self, file_id: int, new_path: str) -> FileRecord:
        new_path = self._file_record_service.__secure_additional_path(new_path)
        file_record_to_update: FileRecord = self._file_record_service \
            .get_record_by_id(file_id)
        self._file_service.update_file_path(file_record_to_update, new_path)
        file_record_to_update = self._file_record_service \
            .update_record_path(file_id, new_path)
        return file_record_to_update

    def test_sync_storage_data(self):
        # given
        file_records = self.__get_test_file_records()
        filepaths = []
        record_id = 1
        expected_record = create_test_file_record(record_id)
        self.__record_repo.get_file_record_by_id.return_value = expected_record

        # when
        actual_record = self.__record_service.get_record_by_id(record_id)

        # then
        self.assertEqual(actual_record, expected_record)
        self.__record_repo.get_file_record_by_id.assert_called_once_with(
            record_id
        )
        self.__session.begin_nested.assert_called_once()
        self.__session_transaction.commit.assert_called_once()
        self.__session_transaction.rollback.assert_not_called()
