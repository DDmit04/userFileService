import collections
import os
import unittest
from io import BytesIO
from unittest import mock
from unittest.mock import Mock

from werkzeug.datastructures import FileStorage

from exception.file.file_not_found_exception import FileNotFoundException
from repository.file_repo.file_repository import FileRepository
from service.file_service.file_service import FileService
from test.test_utils.file_record_utils import FileRecordTestHelper
from utils.data_utils import get_random_filestats


class FileServiceTest(unittest.TestCase):

    def setUp(self):
        self.__path_separator: str = '/'
        self.__upload_dir: str = '/dir'
        self.__file_repo = Mock(spec=FileRepository)
        self.__file_service = FileService(
            self.__upload_dir,
            self.__path_separator,
            self.__file_repo
        )
        self.__file_record_helper = FileRecordTestHelper(self.__path_separator)
        self.__common_additional_path = self.__path_separator.join(
            ["path", "common"]
        )
        self.__common_new_additional_path = self.__path_separator.join(
            ["path", "common", "new"]
        )
        self.__common_filename = "name"
        self.__common_new_filename = "new_name"
        self.__common_file_ext = '.ext'
        self.__test_filepaths_count = 5

    def __get_full_common_filename(self):
        return self.__common_filename + self.__common_file_ext

    def __get_common_filepath(self):
        return self.__path_separator.join(
            [
                self.__common_new_additional_path,
                self.__get_full_common_filename()
            ]
        )

    def test_save_file(self):
        # given
        self.__file_repo.check_file_exists.return_value = True
        additional_path = self.__common_additional_path
        filename = self.__common_filename
        expected_filepath = self.__file_service.get_filepath(
            additional_path,
            filename
        )
        file = Mock(spec=FileStorage, filename=filename)
        # when
        self.__file_service.save_file(file, additional_path)
        # then
        self.__file_repo.save_file \
            .assert_called_once_with(file, expected_filepath)

    def test_delete_file(self):
        # given
        self.__file_repo.check_file_exists.return_value = True
        additional_path = self.__common_additional_path
        filename = self.__common_filename
        expected_filepath = self.__file_service.get_filepath(
            additional_path,
            filename
        )
        # when
        self.__file_service.delete_file(additional_path, filename)
        # then
        self.__file_repo.check_file_exists \
            .assert_called_once_with(expected_filepath)
        self.__file_repo.delete_file.assert_called_once_with(expected_filepath)

    def test_update_filename(self):
        # given
        new_filename = self.__common_new_filename
        updated_record = self.__file_record_helper.create_test_file_record()
        expected_old_filepath = self.__file_service.get_filepath(
            updated_record.path,
            updated_record.get_full_filename()
        )
        expected_new_filepath = self.__file_service.get_filepath(
            updated_record.path,
            new_filename + updated_record.extension
        )
        # when
        self.__file_service.update_filename(updated_record, new_filename)
        # then
        self.__file_repo.check_file_exists.assert_called_once_with(
            expected_old_filepath
        )
        self.__file_repo.update_filename.assert_called_once_with(
            expected_old_filepath,
            expected_new_filepath
        )

    def test_update_file_path(self):
        # given
        new_path = self.__common_new_additional_path
        updated_record = self.__file_record_helper.create_test_file_record()
        expected_old_filepath = self.__file_service.get_filepath(
            updated_record.path,
            updated_record.get_full_filename()
        )
        expected_new_filepath = self.__file_service.get_filepath(
            new_path,
            updated_record.get_full_filename()
        )
        # when
        self.__file_service.update_file_path(updated_record, new_path)
        # then
        self.__file_repo.check_file_exists.assert_called_once_with(
            expected_old_filepath
        )
        self.__file_repo.update_file_path.assert_called_once_with(
            expected_old_filepath,
            expected_new_filepath
        )

    def test_get_filepath_check_exists(self):
        # given
        add_path = self.__common_additional_path
        filename = self.__common_filename
        self.__file_repo.check_file_exists.return_value = True
        expected_filepath = self.__file_service.get_filepath(
            add_path,
            filename
        )
        # when
        actual_filepath = self.__file_service.get_filepath_check_exists(
            add_path,
            filename
        )
        # then
        self.assertEqual(
            expected_filepath,
            actual_filepath,
            "Given filepath and checked filepath not matching!"
        )
        self.__file_repo.check_file_exists.assert_called_once_with(
            expected_filepath
        )

    def test_get_filepath_check_exists_failure(self):
        # given
        add_path = self.__common_additional_path
        filename = self.__common_filename
        self.__file_repo.check_file_exists.return_value = False
        expected_filepath = self.__file_service.get_filepath(
            add_path,
            filename
        )
        with self.assertRaises(FileNotFoundException):
            # when
            actual_filepath = self.__file_service.get_filepath_check_exists(
                add_path,
                filename
            )
            # then
            self.__file_repo.check_file_exists.assert_called_once_with(
                expected_filepath
            )

    def test_get_filepath(self):
        # given
        additional_path = self.__common_new_additional_path
        filename = self.__get_full_common_filename()
        additional_folders = additional_path.split(self.__path_separator)
        expected_filepath = self.__upload_dir
        for additional_folder in additional_folders:
            expected_filepath = os.path.join(
                expected_filepath,
                additional_folder
            )
        expected_filepath = os.path.join(expected_filepath, filename)
        # when
        actual_filepath = self.__file_service.get_filepath(
            additional_path,
            filename
        )
        # then
        self.assertEqual(
            expected_filepath,
            actual_filepath,
            "Expected and created filepaths are not matching!"
        )
        self.__file_repo.assert_not_called()

    def test_get_file(self):
        # given
        path = self.__common_new_additional_path
        full_name = self.__get_full_common_filename()
        file_data = 'data'
        file_encoding = "ascii"
        expected_filepath = self.__file_service.get_filepath(
            path,
            full_name
        )
        mocked_open_function = mock.mock_open(
            read_data=file_data.encode(file_encoding)
        )
        with mock.patch("builtins.open", mocked_open_function):
            with open("any filepath") as f:
                expected_buffer = BytesIO(f.read())
        self.__file_repo.load_file.return_value = expected_buffer
        # when
        actual_buffer = self.__file_service.get_file(path, full_name)
        # then
        self.assertEqual(
            expected_buffer.getvalue(),
            actual_buffer.getvalue(),
            "Stored and downloaded files are not equal!"
        )
        self.__file_repo.load_file.assert_called_once_with(expected_filepath)

    def test_get_all_filepaths(self):
        # given
        expected_paths = self.__file_record_helper \
            .get_test_existed_filepaths(self.__test_filepaths_count)
        self.__file_repo.get_all_files_paths.return_value = expected_paths
        # when
        actual_paths = self.__file_service.get_all_filepaths(self.__upload_dir)
        # then
        self.assertTrue(collections.Counter(actual_paths) == \
                        collections.Counter(expected_paths),
                        "Expected and given file paths are not matching!")
        self.__file_repo.get_all_files_paths.assert_called_once_with(
            self.__upload_dir
        )

    def test_get_file_stats_by_path(self):
        # given
        full_path = self.__get_common_filepath()
        expected_stats = get_random_filestats()
        self.__file_repo.get_file_stats.return_value = expected_stats
        # when
        actual_stats = self.__file_service.get_file_stats_by_path(full_path)
        # then
        self.assertEqual(
            expected_stats,
            actual_stats,
            "Stored and checked files stats are not equal!"
        )
        self.__file_repo.get_file_stats.assert_called_once_with(full_path)
