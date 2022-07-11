import os
import pathlib

from werkzeug.datastructures import FileStorage

from model.dto.fIle_stats_dto import FileStatsDto


def get_file_stats(file: FileStorage) -> FileStatsDto:
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    filename = file.filename
    name = pathlib.Path(filename).stem
    extension = pathlib.Path(filename).suffix
    file_stats_dto = FileStatsDto(name, extension, size)
    return file_stats_dto
