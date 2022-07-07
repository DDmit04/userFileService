from dataclasses import dataclass


@dataclass
class FileStatsDto:
    filename: str
    ext: str
    size: str
    full_path: str

    def get_full_filename(self):
        return f"{self.filename}{self.ext}"
