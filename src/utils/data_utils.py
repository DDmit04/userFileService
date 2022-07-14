from datetime import datetime

from model.dto.add_file_record_request import AddFileRecordRequest
from model.file_record import FileRecord


def create_new_file_record(add_record_request: AddFileRecordRequest,
                           created: datetime = None,
                           updated: datetime = None) -> FileRecord:
    current_date = datetime.now()
    current_date_iso = current_date.isoformat()
    if created is not None:
        current_date_iso = created.isoformat()
    new_file: FileRecord = FileRecord(
        name=add_record_request.name,
        extension=add_record_request.extension,
        size=add_record_request.size,
        path=add_record_request.path,
        created_at=current_date_iso,
        updated_at=updated,
        comment=add_record_request.comment
    )
    return new_file


# TODO make random
def create_test_file_record(rec_id: int = 1) -> FileRecord:
    updated_record = FileRecord()
    updated_record.id = rec_id
    updated_record.name = 'name'
    updated_record.extension = '.ext'
    updated_record.size = 100
    updated_record.path = '/path'
    updated_record.created_at = datetime.now()
    updated_record.updated_at = datetime.now()
    updated_record.comment = 'comment'
    return updated_record
