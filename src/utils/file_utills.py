import os
import pathlib

from werkzeug.datastructures import FileStorage

from model.dto.in_memory_fIle_stats_dto import InMemoryFileStatsDto


def get_file_stats(file: FileStorage) -> InMemoryFileStatsDto:
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    filename = file.filename
    name = pathlib.Path(filename).stem
    extension = pathlib.Path(filename).suffix
    file_stats_dto = InMemoryFileStatsDto(name, extension, size)
    return file_stats_dto
