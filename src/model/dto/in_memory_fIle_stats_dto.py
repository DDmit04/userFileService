from dataclasses import dataclass


@dataclass
class InMemoryFileStatsDto:
    filename: str
    ext: str
    size: str

    def get_full_filename(self):
        return f"{self.filename}{self.ext}"
