import unittest
from unittest import mock
from unittest.mock import Mock

from werkzeug.datastructures import FileStorage

from model.dto.add_file_record_request import AddFileRecordRequest
from model.file_record import FileRecord
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.file_service_facade import FileServiceFacade
from test.test_utils.file_record_utils import FileRecordTestHelper
from test.test_utils.session_utils import SessionTestHelper
from utils.file_utills import get_file_stats


class FileServiceFacadeTest(unittest.TestCase):

    def setUp(self):
        self.__path_separator = '/'
        self.__session_test_helper = SessionTestHelper()
        self.__file_record_service = Mock(spec=FileRecordService)
        self.__file_service = Mock(spec=FileService)
        self.__file_service_facade = FileServiceFacade(
            self.__session_test_helper.session_mock,
            self.__file_service,
            self.__file_record_service
        )
        self.__file_record_helper = FileRecordTestHelper(self.__path_separator)
        self.__common_file_id = 1
        self.__common_additional_path = '/dir/path'
        self.__common_comment = 'comment'
        self.__common_file_data = 'data'
        self.__common_new_filename = 'new_name'
        self.__common_new_filepath = '/path/new/dir'

    def test_add_file(self):
        # given
        additional_path = self.__common_additional_path
        comment = self.__common_comment
        file_data = self.__common_file_data
        file_encoding = "ascii"
        mocked_open_function = mock.mock_open(
            read_data=file_data.encode(file_encoding)
        )
        with mock.patch("builtins.open", mocked_open_function):
            with open("any filepath") as f:
                file = FileStorage(f)
                file_stats = get_file_stats(file)
                add_file_record_request = AddFileRecordRequest(
                    file_stats.filename,
                    file_stats.ext,
                    file_stats.size,
                    additional_path,
                    comment
                )
                expected_file_record = FileRecord(
                    self.__common_file_id, file_stats.filename,
                    file_stats.ext, file_stats.size,
                    additional_path, None,
                    None, comment
                )
                self.__file_record_service.add_new_file_record_by_request \
                    .return_value = expected_file_record
                self.__file_record_service.secure_additional_path.return_value = \
                    additional_path
                # when
                actual_file_record = self.__file_service_facade.add_file(
                    file,
                    additional_path,
                    comment
                )
                # then
                self.assertEqual(
                    actual_file_record,
                    expected_file_record,
                    "Saved FileRecord not match with expected!"
                )
                self.__file_record_service.add_new_file_record_by_request \
                    .assert_called_once_with(add_file_record_request)
                self.__file_service.save_file.assert_called_once_with(
                    file,
                    additional_path
                )
                self.__session_test_helper.assert_session_commit()

    def test_delete_file(self):
        # given
        file_id = self.__common_file_id
        deleted_file_record = self.__file_record_helper \
            .create_test_file_record(file_id)
        self.__file_record_service \
            .get_record_by_id.return_value = deleted_file_record
        # when
        self.__file_service_facade.delete_file(file_id)
        # then
        self.__file_record_service.delete_file_record \
            .assert_called_once_with(file_id)
        self.__file_service.delete_file.assert_called_once_with(
            deleted_file_record.path,
            deleted_file_record.get_full_filename()
        )
        self.__session_test_helper.assert_session_commit()

    def test_update_filename(self):
        # given
        file_id = self.__common_file_id
        new_name = self.__common_new_filename
        updating_file_record = self.__file_record_helper \
            .create_test_file_record(file_id)
        self.__file_record_service.get_record_by_id.return_value \
            = updating_file_record
        # when
        self.__file_service_facade.update_filename(
            file_id,
            new_name
        )
        # then
        self.__file_record_service.get_record_by_id. \
            assert_called_once_with(file_id)
        self.__file_service.update_filename.assert_called_once_with(
            updating_file_record,
            new_name
        )
        self.__file_record_service.update_record_name. \
            assert_called_once_with(file_id, new_name)
        self.__session_test_helper.assert_session_commit()

    def update_file_path(self):
        # given
        file_id = self.__common_file_id
        new_path = self.__common_new_filepath
        updating_file_record = self.__file_record_helper \
            .create_test_file_record(self.__path_separator, file_id)
        # when
        self.__file_service_facade.update_file_path(
            file_id,
            new_path
        )
        # then
        self.__file_record_service.get_record_by_id. \
            assert_called_once_with(file_id)
        self.__file_service.update_filename.assert_called_once_with(
            updating_file_record,
            new_path
        )
        self.__file_record_service.update_record_name. \
            assert_called_once_with(file_id, new_path)
        self.__session_test_helper.assert_session_commit()
