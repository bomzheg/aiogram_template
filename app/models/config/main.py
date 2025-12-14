from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from app.models.config.db import DBConfig, DBConfigProperties, RedisConfig
from app.models.config.storage import StorageConfig


@dataclass(kw_only=True)
class Config:
    paths: Paths
    db: DBConfig
    redis: RedisConfig
    bot: BotConfig

    @property
    def app_dir(self) -> Path:
        return self.paths.app_dir

    @property
    def config_path(self) -> Path:
        return self.paths.config_path

    @property
    def log_path(self) -> Path:
        return self.paths.log_path


@dataclass(kw_only=True, frozen=True, slots=True)
class _Config:
    db: DBConfigProperties
    redis: RedisConfig
    bot: BotConfig


@dataclass(kw_only=True, frozen=True, slots=True)
class Paths:
    app_dir: Path

    @property
    def config_path(self) -> Path:
        return self.app_dir / "config"

    @property
    def logging_config_file(self) -> Path:
        return self.config_path / "logging.yaml"

    @property
    def log_path(self) -> Path:
        return self.app_dir / "log"


@dataclass(kw_only=True, frozen=True, slots=True)
class BotConfig:
    token: str
    log_chat: int
    superusers: list[int]
    bot_api: BotApiConfig
    storage: StorageConfig


@dataclass(kw_only=True, slots=True, frozen=True)
class BotApiConfig:
    type: BotApiType
    botapi_url: str | None = None
    botapi_file_url: str | None = None

    @property
    def is_local(self) -> bool:
        return self.type == BotApiType.local


class BotApiType(Enum):
    official = "official"
    local = "local"
