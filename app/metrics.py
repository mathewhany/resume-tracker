from io import TextIOWrapper
import json
from typing import Protocol


class MetricsManager(Protocol):
    def record_visit(self, page: str, source: str) -> None:
        ...

    def get_count(self, page: str) -> dict[str, int]:
        ...

    def get_all_counts(self) -> dict[str, dict[str, int]]:
        ...


class JSONMetricsManager:
    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file

    def record_visit(self, page: str, source: str) -> None:
        data = self.get_all_counts()
        data[page] = data.get(page, {})
        data[page][source] = data[page].get(source, 0) + 1

        self.file.seek(0)
        self.file.truncate()
        json.dump(data, self.file)
        self.file.seek(0)

    def get_count(self, page: str) -> dict[str, int]:
        return self.get_all_counts().get(page, {})

    def get_all_counts(self) -> dict[str, dict[str, int]]:
        self.file.seek(0)

        if not self.file.read():
            return {}

        self.file.seek(0)
        result = json.load(self.file)
        self.file.seek(0)

        return result
