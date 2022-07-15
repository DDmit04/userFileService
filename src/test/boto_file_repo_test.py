import collections
import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock

from boto3.resources.base import ServiceResource

from repository.file_repo.boto_file_repository import BotoFileRepository
from test.test_utils.file_record_utils import FileRecordTestHelper


class BotoFileRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.__path_separator = '/'
        self.__boto_client = Mock(spec=ServiceResource)
        self.__boto_client.upload_fileobj = MagicMock()
        self.__boto_client.delete_object = MagicMock()
        self.__boto_client.list_objects = MagicMock()
        self.__boto_client.head_object = MagicMock()
        self.__boto_client.download_fileobj = MagicMock()
        self.__boto_client.list_objects_v2 = MagicMock()
        self.__boto_client.copy_object = MagicMock()

        self.__default_bucket_name = 'default'
        self.__boto_file_repo = BotoFileRepository(
            self.__boto_client,
            self.__default_bucket_name
        )
        self.__file_record_helper = FileRecordTestHelper(self.__path_separator)
        self.__test_records_count = 5
        self.__common_filepath = '/path/dir'
        self.__common_old_filepath = '/old/path/dir'
        self.__common_new_filepath = '/new/path/dir'

    def test_save_file(self):
        # given
        filepath = self.__common_filepath
        bucket_name = self.__default_bucket_name
        file_data = 'data'
        file_encoding = "ascii"
        mocked_open_function = mock.mock_open(
            read_data=file_data.encode(file_encoding)
        )
        with mock.patch("builtins.open", mocked_open_function):
            with open("any filepath") as file:
                # when
                self.__boto_file_repo.save_file(file, filepath)
                # then
                self.__boto_client.upload_fileobj.assert_called_once_with(
                    file, bucket_name, filepath
                )

    def test_delete_file(self):
        # given
        filepath = self.__common_filepath
        bucket_name = self.__default_bucket_name
        # when
        self.__boto_file_repo.delete_file(filepath)
        # then
        self.__boto_client.delete_object.assert_called_once_with(
            Bucket=bucket_name,
            Key=filepath
        )

    def test_get_all_files_paths(self):
        # given
        dir_path = self.__common_filepath
        bucket_name = self.__default_bucket_name
        expected_paths = self.__file_record_helper.get_test_existed_filepaths(
            self.__test_records_count
        )
        boto_response = {
            "Contents": [{"Key": path} for path in expected_paths]
        }
        self.__boto_client.list_objects.return_value = boto_response
        # when
        actual_paths = self.__boto_file_repo.get_all_files_paths(dir_path)
        # then
        self.assertEqual(
            collections.Counter(expected_paths),
            collections.Counter(actual_paths)
        )
        self.__boto_client.list_objects.assert_called_once_with(
            Bucket=bucket_name,
            Prefix=dir_path
        )

    def test_update_filepath_or_name(self):
        # given
        old_filepath = self.__common_old_filepath
        new_filepath = self.__common_new_filepath
        bucket_name = self.__default_bucket_name
        copy_source = {
            'Bucket': bucket_name,
            'Key': old_filepath
        }
        # when
        self.__boto_file_repo.update_file_path(old_filepath, new_filepath)
        # then
        self.__boto_client.copy_object.assert_called_once_with(
            Bucket=bucket_name,
            CopySource=copy_source,
            Key=new_filepath
        )
        self.__boto_client.delete_object.assert_called_once_with(
            Bucket=bucket_name,
            Key=old_filepath
        )

    def test_check_file_exists(self):
        # given
        filepath = self.__common_filepath
        bucket_name = self.__default_bucket_name
        # when
        actual_exists = self.__boto_file_repo.check_file_exists(filepath)
        # then
        self.assertTrue(actual_exists)
        self.__boto_client.head_object.assert_called_once_with(
            Bucket=bucket_name,
            Key=filepath
        )

    def test_get_file_stats(self):
        # given
        filepath = self.__common_filepath
        bucket_name = self.__default_bucket_name
        expected_file_stats = self.__file_record_helper \
            .get_test_stored_file_stats()
        self.__boto_client.list_objects_v2.return_value = {
            "Contents": [{
                "Size": expected_file_stats.size,
                "LastModified": expected_file_stats.updated
            }]
        }
        # when
        actual_file_stats = self.__boto_file_repo.get_file_stats(filepath)
        # then
        self.assertEqual(expected_file_stats.size, actual_file_stats.size)
        self.assertEqual(expected_file_stats.updated,
                         actual_file_stats.updated)
        self.__boto_client.list_objects_v2.assert_called_once_with(
            Bucket=bucket_name,
            Prefix=filepath
        )
