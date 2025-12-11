from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum

from app.models.config.db import RedisConfig

logger = logging.getLogger(__name__)


class StorageType(Enum):
    memory = "memory"
    redis = "redis"


@dataclass
class StorageConfig:
    type_: StorageType
    redis: RedisConfig | None = None

    def __post_init__(self) -> None:
        if self.type_ is StorageType.redis and self.redis is None:
            raise ValueError("you have to specify redis config for use redis storage")
