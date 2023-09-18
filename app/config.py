from dataclasses import dataclass
import os
from typing import Protocol


@dataclass
class Config:
    resume_url: str

    def validate(self) -> dict[str, list[str]]:
        errors = {}
        if not self.resume_url:
            errors["resume_url"] = ["Missing resume URL"]
        return errors


class ConfigProvider(Protocol):
    def get_config(self) -> Config:
        pass


class EnvironmentConfigProvider:
    def get_config(self) -> Config:
        return Config(resume_url=os.environ.get("RESUME_URL"))
