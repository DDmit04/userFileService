import unittest
from datetime import datetime
from unittest.mock import Mock

from model.file_record import FileRecord
from repository.file_record_repository import FileRecordRepository
from service.file_record_service import FileRecordService
from test.test_utils.file_record_utils import FileRecordTestHelper
from test.test_utils.session_utils import SessionTestHelper
from utils.data_utils import create_new_file_record


class FileRecordServiceTest(unittest.TestCase):

    def setUp(self):
        self.__record_repo = Mock(spec=FileRecordRepository)
        self.__session_test_helper = SessionTestHelper()
        self.__path_separator: str = '/'
        self.__record_service = FileRecordService(
            self.__session_test_helper.session_mock,
            self.__record_repo,
            self.__path_separator
        )
        self.__file_record_helper = FileRecordTestHelper(self.__path_separator)
        self.__common_record_id = 1
        self.__test_records_count = 5
        self.__common_new_comment = 'comment'
        self.__common_new_path = '/path/new/dir'
        self.__common_new_filename = 'new_name'
        self.__common_search_dir = '/dir'

    def test_add_new_file_record(self):
        # given
        add_file_record_request = \
            self.__file_record_helper.create_add_file_record_request()
        creation_time = datetime.now()
        update_time = datetime.now()
        new_file_record = create_new_file_record(
            add_file_record_request,
            creation_time,
            update_time
        )
        self.__record_repo.find_record_by_full_path.return_value = None
        # when
        self.__record_service.add_new_file_record(
            add_file_record_request,
            creation_time,
            update_time
        )
        # then
        self.__record_repo.find_record_by_full_path.assert_called_once_with(
            new_file_record.path,
            new_file_record.name,
            new_file_record.extension
        )
        self.__record_repo.save_file_record.assert_called_once_with(
            new_file_record
        )
        self.__session_test_helper.assert_session_commit()

    @unittest.skip
    def test_add_new_file_record_by_request(self):
        # given
        self.__record_repo.find_record_by_full_path.return_value = None
        add_file_record_request = self.__create_add_file_record_request()
        new_file_record = create_new_file_record(add_file_record_request)
        # when
        self.__record_service.add_new_file_record_by_request(
            add_file_record_request
        )
        # then
        self.__record_repo.find_record_by_full_path.assert_called_once_with(
            new_file_record.path,
            new_file_record.name,
            new_file_record.extension
        )
        self.__record_repo.save_file_record.assert_called_once_with(
            new_file_record
        )
        self.__session_test_helper.assert_session_commit()

    def test_delete_file_record(self):
        # given
        record_id = self.__common_record_id
        # when
        self.__record_service.delete_file_record(record_id)
        # then
        self.__record_repo.delete_file_record_by_id.assert_called_once_with(
            record_id
        )
        self.__session_test_helper.assert_session_commit()

    def test_list_files_records(self):
        # given
        expected_records = self.__file_record_helper \
            .get_test_file_records(self.__test_records_count)
        self.__record_repo.get_all_files_records.return_value \
            = expected_records
        # when
        actual_records = self.__record_service.list_files_records()
        # then
        self.assertSetEqual(
            set(expected_records),
            set(actual_records),
            "Expected and actual set of records are not equal!"
        )
        self.__record_repo.get_all_files_records.assert_called_once()
        self.__session_test_helper.assert_session_commit()

    def test_get_file_record(self):
        # given
        record_id = self.__common_record_id
        expected_file_record = self.__file_record_helper. \
            create_test_file_record(record_id)
        self.__record_repo.get_file_record_by_id.return_value = \
            expected_file_record
        # when
        actual_record = self.__record_service.get_file_record(record_id)
        # then
        self.assertEqual(
            actual_record,
            expected_file_record,
            "Requested and actual FileRecords are not equal!"
        )
        self.__record_repo.get_file_record_by_id.assert_called_once_with(
            record_id
        )
        self.__session_test_helper.assert_session_commit()

    @unittest.skip
    def test_update_record_comment(self):
        # given
        record_id = self.__common_record_id
        new_comment = self.__common_new_comment
        update_dict = {FileRecord.comment: new_comment}
        # when
        self.__record_service.update_record_comment(record_id, new_comment)
        # then
        self.__record_repo.update_file_record.assert_called_once_with(
            record_id,
            update_dict
        )
        self.__session_test_helper.assert_session_commit()

    @unittest.skip
    def test_update_record_name(self):
        # given
        record_id = self.__common_record_id
        new_name = self.__common_new_filename
        update_dict = {FileRecord.name: new_name}
        # when
        self.__record_service.update_record_name(record_id, new_name)
        # then
        self.__record_repo.update_file_record.assert_called_once_with(
            record_id,
            update_dict
        )
        self.__session_test_helper.assert_session_commit()

    @unittest.skip
    def test_update_record_path(self):
        # given
        record_id = self.__common_record_id
        new_path = self.__common_new_path
        update_dict = {FileRecord.path: new_path}
        # when
        self.__record_service.update_record_path(record_id, new_path)
        # then
        self.__record_repo.update_file_record.assert_called_once_with(
            record_id,
            update_dict
        )
        self.__session_test_helper.assert_session_commit()

    def test_get_records_on_dir(self):
        # given
        dir_level = self.__common_search_dir
        expected_records = self.__file_record_helper \
            .get_test_file_records(self.__test_records_count)
        self.__record_repo.get_file_records_with_path.return_value \
            = expected_records
        # when
        actual_records = self.__record_service.get_records_on_dir(dir_level)
        # then
        self.assertSetEqual(
            set(expected_records),
            set(actual_records),
            "Expected and actual set of records by dir are not equal!"
        )
        self.__record_repo.get_file_records_with_path \
            .assert_called_once_with(dir_level)
        self.__session_test_helper.assert_session_commit()

    def test_get_record_by_id(self):
        # given
        record_id = self.__common_record_id
        expected_record = self.__file_record_helper \
            .create_test_file_record(record_id)
        self.__record_repo.get_file_record_by_id.return_value = expected_record
        # when
        actual_record = self.__record_service.get_record_by_id(record_id)
        # then
        self.assertEqual(
            actual_record,
            expected_record,
            "Expected and actual FileRecord are not equal!"
        )
        self.__record_repo.get_file_record_by_id.assert_called_once_with(
            record_id
        )
        self.__session_test_helper.assert_session_commit()
