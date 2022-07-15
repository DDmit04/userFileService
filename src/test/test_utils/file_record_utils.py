import random
from datetime import datetime

from model.dto.add_file_record_request import AddFileRecordRequest
from model.dto.stored_fIle_stats_dto import StoredFileStatsDto
from model.file_record import FileRecord
from utils.data_utils import get_random_string, get_random_filename


class FileRecordTestHelper:

    def __init__(self, path_separator: str):
        super().__init__()
        self.__path_separator = path_separator

    def create_test_file_record(self, rec_id: int = 1) -> FileRecord:
        updated_record = FileRecord(
            rec_id,
            get_random_string(5),
            f'.{get_random_string(3)}',
            random.randint(100, 2000),
            self.__path_separator.join(
                [get_random_string(5), get_random_string(5)]
            ),
            datetime.now(),
            datetime.now(),
            get_random_string(10)
        )
        return updated_record

    def create_add_file_record_request(self) -> \
            AddFileRecordRequest:
        request = AddFileRecordRequest(
            get_random_string(5),
            f'.{get_random_string(3)}',
            random.randint(100, 2000),
            self.__path_separator.join(
                [get_random_string(5), get_random_string(5)]
            ),
            get_random_string(10)
        )
        return request

    def get_test_file_records(self, test_records_count: int) \
            -> list[FileRecord]:
        expected_records = []
        for i in range(test_records_count):
            file_record = self.create_test_file_record(i)
            expected_records.append(file_record)
        return expected_records

    def get_test_existed_filepaths(self, paths_count: int):
        paths = []
        for i in range(paths_count):
            paths.append(
                self.__path_separator.join(
                    [
                        get_random_string(5),
                        get_random_string(5),
                        get_random_filename()
                    ]
                )
            )
        return paths

    def get_test_stored_file_stats(self):
        expected_file_stats = StoredFileStatsDto(
            random.randint(100, 2000),
            datetime.now(),
            datetime.now()
        )
        return expected_file_stats
