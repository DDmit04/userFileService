import random
import string
from datetime import datetime

from model.dto.add_file_record_request import AddFileRecordRequest
from model.dto.stored_fIle_stats_dto import StoredFileStatsDto
from model.file_record import FileRecord


def create_new_file_record(add_record_request: AddFileRecordRequest,
                           created: datetime = None,
                           updated: datetime = None) -> FileRecord:
    current_date = datetime.now()
    current_date_iso = current_date.isoformat()
    if created is not None:
        current_date_iso = created.isoformat()
    new_file: FileRecord = FileRecord(
        None,
        name=add_record_request.name,
        extension=add_record_request.extension,
        size=add_record_request.size,
        path=add_record_request.path,
        created_at=current_date_iso,
        updated_at=updated,
        comment=add_record_request.comment
    )
    return new_file


def get_random_string(length: int) -> str:
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _
        in range(length))


def get_random_filename() -> str:
    return f'{get_random_string(5)}.{get_random_string(3)}'


def get_random_filestats() -> StoredFileStatsDto:
    res = StoredFileStatsDto(
        random.randint(100, 2000),
        datetime.now(),
        datetime.now()
    )
    return res
