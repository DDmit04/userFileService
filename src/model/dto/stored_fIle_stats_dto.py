from dataclasses import dataclass
from datetime import datetime


@dataclass
class StoredFileStatsDto:
    size: int
    created: datetime
    updated: datetime

    def get_full_filename(self):
        return f"{self.filename}{self.ext}"
