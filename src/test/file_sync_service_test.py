import os
import unittest
from unittest.mock import Mock

from model.dto.stored_fIle_stats_dto import StoredFileStatsDto
from service.file_record_service import FileRecordService
from service.file_service.file_service import FileService
from service.file_sync_service import FileSyncService
from test.test_utils.file_record_utils import FileRecordTestHelper
from test.test_utils.session_utils import SessionTestHelper
from utils.data_utils import get_random_filestats


class FileSyncServiceTest(unittest.TestCase):

    def setUp(self):
        self.__session_test_helper = SessionTestHelper()
        self.__upload_dir = "/upload"
        self.__path_separator = "/"
        self.__file_record_service = Mock(spec=FileRecordService)
        self.__file_service = Mock(spec=FileService)
        self.__file_sync_service = FileSyncService(
            self.__session_test_helper.session_mock,
            self.__upload_dir,
            self.__path_separator,
            self.__file_record_service,
            self.__file_service
        )
        self.__file_record_helper = FileRecordTestHelper(self.__path_separator)
        self.__test_records_count = 5

    def __get_filepath_effect(self, path: str, filename: str) -> str:
        additional_folders = path.split(self.__path_separator)
        filepath = self.__upload_dir
        for additional_folder in additional_folders:
            filepath = os.path.join(filepath, additional_folder)
        filepath = os.path.join(filepath, filename)
        return filepath

    def __get_filestats(self, path: str) -> StoredFileStatsDto:
        return get_random_filestats()

    def test_sync_storage_data(self):
        # given
        file_records = self.__file_record_helper \
            .get_test_file_records(self.__test_records_count)
        matching_filepaths = self \
            .__get_full_filepaths_from_records(file_records)
        self.__setup_services_behavior(file_records, matching_filepaths)
        # when
        self.__file_sync_service.sync_storage_data()
        # then
        self.assertEqual(
            self.__test_records_count,
            self.__file_service.get_filepath.call_count,
            "Get filepath was not called for all records!"
        )
        self.__file_record_service.delete_file_record.assert_not_called()
        self.__file_service.get_file_stats_by_path.assert_not_called()
        self.__file_record_service.add_new_file_record.assert_not_called()
        self.__session_test_helper.assert_session_commit()

    def __get_full_filepaths_from_records(self, file_records):
        return list(
            map(lambda record: self.__path_separator
                .join(
                [
                    self.__upload_dir,
                    record.path,
                    record.get_full_filename()
                ]),
                file_records)
        )

    def __setup_services_behavior(self, file_records, real_filepaths):
        self.__file_record_service.list_files_records \
            .return_value = file_records
        self.__file_service.get_all_filepaths.return_value = real_filepaths
        self.__file_service.get_filepath.side_effect = \
            self.__get_filepath_effect
        self.__file_service.get_file_stats_by_path.side_effect \
            = self.__get_filestats

    def test_sync_storage_data_delete_records(self):
        # given
        file_records = self.__file_record_helper \
            .get_test_file_records(self.__test_records_count)
        matching_filepaths = []
        self.__setup_services_behavior(file_records, matching_filepaths)
        # when
        self.__file_sync_service.sync_storage_data()
        # then
        self.assertEqual(
            self.__test_records_count,
            self.__file_service.get_filepath.call_count,
            "Get filepath was not called for all records!"
        )
        self.assertEqual(
            self.__test_records_count,
            self.__file_record_service.delete_file_record.call_count,
            "Not all orphan file records were deleted!"
        )
        self.__file_service.get_file_stats_by_path.assert_not_called()
        self.__file_record_service.add_new_file_record.assert_not_called()
        self.__session_test_helper.assert_session_commit()

    def test_sync_storage_data_restore_records(self):
        # given
        file_records = []
        matching_filepaths = self.__get_full_filepaths_from_records(
            self.__file_record_helper.get_test_file_records(
                self.__test_records_count
            )
        )
        self.__setup_services_behavior(file_records, matching_filepaths)
        # when
        self.__file_sync_service.sync_storage_data()
        # then
        self.assertEqual(
            self.__test_records_count,
            self.__file_service.get_file_stats_by_path.call_count,
            "Get filestats was not called for all missing files!"
        )
        self.assertEqual(
            self.__test_records_count,
            self.__file_record_service.add_new_file_record.call_count,
            "Not all missing FileRecords were saved!"
        )
        self.__file_service.get_filepath.assert_not_called()
        self.__file_record_service.delete_file_record.assert_not_called()
        self.__session_test_helper.assert_session_commit()
