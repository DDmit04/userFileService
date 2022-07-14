import unittest
from unittest.mock import Mock

from sqlalchemy.orm import Session, SessionTransaction

from model.dto.add_file_record_request import AddFileRecordRequest
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.file_sync_service import FileSyncService
from utils.data_utils import create_test_file_record


class FileSyncServiceTest(unittest.TestCase):

    def setUp(self):
        self.__session = Mock(spec=Session)
        self.__session_transaction = Mock(spec=SessionTransaction)
        self.__session.begin_nested.return_value = self.__session_transaction
        self.__upload_dir = "/upload"
        self.__path_separator = "/"
        self.__file_record_service = Mock(spec=FileRecordService)
        self.__file_service = Mock(spec=FileService)
        self.__file_sync_service = FileSyncService(
            self.__session,
            self.__upload_dir_path,
            self.__path_separator,
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
